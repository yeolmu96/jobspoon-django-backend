from abc import ABC, abstractmethod

from interview_result.entity.interview_result import InterviewResult
from interview_result.entity.interview_result_qas import InterviewResultQAS
from interview_result.repository.interview_result_repository import InterviewResultRepository
from interview_result.entity.interview_result_score import InterviewResultScore

class InterviewResultRepositoryImpl(InterviewResultRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def registerInterviewResult(self, account):
        InterviewResult.objects.create(account=account)
        interviewResult = InterviewResult.objects.all()
        return interviewResult.last()


    def registerInterviewResultQAS(self, interviewResult, scoreResultList):
        for scoreResult in scoreResultList:
            print(scoreResult)
            question, answer, intent, feedback = scoreResult
            if len(answer) <= 30:
                feedback = '10점<s>답변의 길이가 너무 짧습니다. 질문과 관련한 당신의 구체적인 사례를 언급하여 답변한다면 좋은 점수를 받을 수 있습니다.'
                if any(keyword in answer for keyword in ['모르', '못했', '몰라', '죄송', '모름', '못하']):
                    feedback = '0점<s>답변의 길이가 너무 짧으며, 질문의 의도와 맞지 않습니다. 어려운 질문이라도 최대한 답변할 수 있는 내용을 작성하는 것이 좋습니다.'

            InterviewResultQAS.objects.create(question=question, answer=answer, intent=intent,
                                              feedback=feedback, interview_result=interviewResult)

    def getLastInterviewResult(self,account):
        result = InterviewResult.objects.filter(account=account).order_by('-id').first()
        print(f"▶ getLastInterviewResultByAccount() → {result}")
        return result

    def getLastInterviewResultQASList(self, interviewResult):
        query = InterviewResultQAS.objects.filter(interview_result=interviewResult)
        print(f"▶ QAS count: {query.count()}")  # 0이면 인터뷰에 QAS가 없음

        interviewResultQASList = query.order_by('id').values_list('question', 'answer', 'intent', 'feedback')
        print(f"▶ QAS values_list: {list(interviewResultQASList)}")  # 튜플 리스트로 출력

        return interviewResultQASList

    # def saveInterviewResult(self, accountId):
    #     try:
    #         interviewResult = InterviewResult.objects.create(account_id=accountId)
    #         print("✅ 면접 완료 기록 저장")
    #         return interviewResult
    #     except Exception as e:
    #         print(f"❌ 오류 발생: {e}")
    #         raise

    # ✅ 수정된 저장 로직
    def saveInterviewResult(self, accountId: int, interviewId: int):
        try:
            interviewResult = InterviewResult.objects.create(
                account_id=accountId,
                interview_id=interviewId  # ✅ 추가됨
            )
            print("✅ 면접 완료 기록 저장")
            return interviewResult
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            raise

    def saveQAScoreList(self, interview_result, qa_scores):
        try:
            for qa in qa_scores:
                question = qa.get("question","")
                answer = qa.get("answer","")
                intent = qa.get("intent","기본") #없으면 기본값
                feedback = qa.get("feedback","피드백 없음")

                InterviewResultQAS.objects.create(
                    interview_result=interview_result,
                    question=question,
                    answer=answer,
                    intent=intent,
                    feedback=feedback
                )
                print("평가 결과 저장 완료")
        except Exception as e:
            print(f"평가 결과 저장 실패: {e}")
            raise

    def saveHexagonScore(self, interview_result, evaluation_scores: dict):
        try:
            InterviewResultScore.objects.create(
                interview_result=interview_result,
                productivity=evaluation_scores.get("productivity", 0.0),
                communication=evaluation_scores.get("communication", 0.0),
                technical_skills=evaluation_scores.get("technical_skills", 0.0),
                documentation_skills=evaluation_scores.get("documentation_skills", 0.0),
                flexibility=evaluation_scores.get("flexibility", 0.0),
                problem_solving=evaluation_scores.get("problem_solving", 0.0),
            )
            print("✅ 6각형 점수 저장 완료")
        except Exception as e:
            print(f"❌ 6각형 점수 저장 실패: {e}")
            raise
