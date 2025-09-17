from django.db import transaction
from django.shortcuts import render
import json, time

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from interview_result.service.interview_result_service_impl import InterviewResultServiceImpl
from interview_result.entity.interview_result import InterviewResult
from interview_result.entity.interview_result_qas import InterviewResultQAS
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from utility.http_client import HttpClient


class InterviewResultController(viewsets.ViewSet):
    interviewResultService = InterviewResultServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    #면접 종료 상태 저장
    def requestEndInterview(self, request):
        try:
            postRequest = request.data
            userToken = postRequest.get("userToken")
            interviewId = postRequest.get("interviewId")

            if not userToken or not interviewId:
                return JsonResponse({
                    "error": "필수 값이 누락되었습니다",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)

            accountId = self.redisCacheService.getValueByKey(userToken)

            # result = self.interviewResultService.saveInterviewResult(accountId)
            # ✅ InterviewResult 저장 (accountId + interviewId)
            result = self.interviewResultService.saveInterviewResult(accountId, interviewId)

            # ✅ Interview 테이블의 status도 COMPLETED로 업데이트
            from interview.entity.interview import Interview
            Interview.objects.filter(id=interviewId, account_id=accountId).update(status="COMPLETED")


            return JsonResponse({
                "message": "면접 완료 기록 저장 성공",
                "interviewResultId": result.id,
                "status": "COMPLETED",   # 👈 프론트에서 확인 가능
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ 면접 저장 실패: {e}")
            return JsonResponse({
                "error": "서버 오류 발생",
                "success": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 요약 생성
    @action(detail=False, methods=["post"])
    def requestInterviewSummary(self, request):
        try:
            data = request.data
            userToken = data.get("userToken")
            interviewId=data.get("interviewId")

            accountId = self.redisCacheService.getValueByKey(userToken)
            interview_result = InterviewResult.objects.filter(account_id=accountId).latest("id")

            context = {
                "userToken": str(userToken),
                "topic": str(data.get("jobCategory")),
                "experienceLevel": str(data.get("experienceLevel")),
                "projectExperience": str(data.get("projectExperience")),
                "academicBackground": str(data.get("academicBackground")),
                "interviewTechStack": json.dumps(data.get("interviewTechStack"))
            }

            questions, answers, questionId = self.interviewResultService.getFullQAList(interviewId)
            if not questions or not answers:
                raise Exception("질문/답변 복원 실패")

            # FastAPI 전송용 payload 생성
            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId, #전체 질문 ID리스트
                #"answerText": "", 마지막 답변에 대한 중요도가 높은경우 사용
                "topic": int(data.get("jobCategory")),
                "experienceLevel": int(data.get("experienceLevel")),
                "projectExperience": int(data.get("projectExperience")),
                "academicBackground": int(data.get("academicBackground")),
                "interviewTechStack": data.get("interviewTechStack"),
                "context": context,
                "questions": questions,
                "answers": answers
            }

            # ✅ FastAPI 요청 후 응답 받기
            response = HttpClient.postToAI("/interview/question/end_interview", payload)
            # polling으로 결과 받기
            for _ in range(60):
                time.sleep(1)
                result = HttpClient.getFromAI(f"/interview/question/check-result/{userToken}")
                if result and result.get("status") == "DONE":
                    response = result.get("result", {})
                    break
                elif result and result.get("status") == "FAILED":
                    raise Exception("FastAPI 평가 실패")
            else:
                raise Exception("FastAPI 응답 대기 시간 초과")
            summary = response.get("summary", "")
            qa_scores = response.get("qa_scores",[])
            evaluation_scores = response.get("evaluation_result", {})  # ✅ 새로 추가된 평가 점수
            print(f"{evaluation_scores}")
            print(f"📄 요약 내용: {summary}")
            print(f"📦 전체 응답: {response}")

            if not qa_scores:
                raise Exception("FastAPI 응답dp qa_scores가 없음")

            #평가 결과 저장
            self.interviewResultService.saveQAScoreList(interview_result, qa_scores)

            # ✅ 6각형 점수 저장
            if evaluation_scores:
                self.interviewResultService.recordHexagonEvaluation(interview_result, evaluation_scores)

            return JsonResponse({
                "message": "면접 평가 저장 성공",
                "summary": summary,
                "qa_scores": qa_scores,
                "success": True
            }, status=200)

        except Exception as e:
            print(f"❌ requestInterviewSummary 오류: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    def getInterviewResult(self, request):
        try:
            userToken = request.data.get("userToken")
            accountId = self.redisCacheService.getValueByKey(userToken)
            interview_result = InterviewResult.objects.filter(account_id=accountId).latest("id")

            result_list = list(
                InterviewResultQAS.objects.filter(interview_result=interview_result)
                .values("question", "answer", "intent", "feedback")
            )

            # ✅ 6각형 점수 불러오기
            score = getattr(interview_result, "score", None)  # related_name='score' 사용

            hexagon_score = {
                "productivity": score.productivity if score else 0,
                "communication": score.communication if score else 0,
                "technical_skills": score.technical_skills if score else 0,
                "documentation_skills": score.documentation_skills if score else 0,
                "flexibility": score.flexibility if score else 0,
                "problem_solving": score.problem_solving if score else 0,
            }

            return JsonResponse({
               "message": "면접 평가 결과 조회 성공",
                "interviewResultList": result_list,
                "hexagonScore": hexagon_score,
                "success": True
            }, status=200)

        except Exception as e:
            print(f"❌ getInterviewEvaluationResult 오류: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)