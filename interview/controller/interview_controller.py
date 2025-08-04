from django.db import transaction
from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from interview.service.interview_service_impl import InterviewServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from utility.http_client import HttpClient


class InterviewController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()
    interviewService = InterviewServiceImpl.getInstance()

    # 사용자 답변 저장 코드
    @action(detail=False, methods=["post"])
    def requestCreateAnswer(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")
        print(f"answerText= {answerText}")

        if not userToken or not interviewId or not questionId or not answerText:
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            with transaction.atomic():
                result = self.interviewService.saveAnswer(
                    accountId=accountId,
                    interviewId=interviewId,
                    questionId=questionId,
                    answerText=answerText
                )

                if not result:
                    raise Exception("답변 저장 실패")

            return JsonResponse({"message": "답변 저장 완료", "success": True})

        except Exception as e:
            print(f"[Error] requestCreateAnswer: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    def requestListInterview(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        page = postRequest.get("page", 1)
        perPage = postRequest.get("perPage", 10)

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            interviewList, totalItems = self.interviewService.listInterview(accountId, page, perPage)

            return JsonResponse({
                "interviewList": interviewList,
                "totalItems": totalItems,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"면접 정보 조회 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def requestRemoveInterview(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("id")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            result = self.interviewService.removeInterview(accountId, interviewId)

            if result["success"]:
                return JsonResponse(result, status=status.HTTP_200_OK)
            else:
                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"면접 정보 제거 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def requestCreateInterview(self, request):
        postRequest = request.data
        print(f"postRequest: {postRequest}")

        userToken = postRequest.get("userToken")
        jobCategory = postRequest.get("jobCategory")
        experienceLevel = postRequest.get("experienceLevel")
        projectExperience = postRequest.get("projectExperience")
        academicBackground = postRequest.get("academicBackground")
        techStack = postRequest.get("interviewTechStack")
        companyName = postRequest.get("companyName")


        # 첫 질문
        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        if (jobCategory is None or experienceLevel is None or projectExperience is None or academicBackground is None or companyName is None):
            return JsonResponse({"error": "필수 항목 누락", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        print(f"userToken 획득")

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"accountId 찾기: {accountId}")

            with transaction.atomic():  # ✅ 트랜잭션 블록 시작
                createdInterview = self.interviewService.createInterview(
                    accountId, jobCategory, experienceLevel,projectExperience, academicBackground, techStack, companyName  # 지금 accountId가 안옴
                )
                print(f"createdInterview : {createdInterview}")

                if createdInterview is None:
                    raise Exception("면접 생성 실패")

                payload = {   # 이 정보만 FastAPI로 전달
                    "userToken": userToken,
                    "interviewId": createdInterview.id,
                    "topic": createdInterview.topic,
                    "experienceLevel": createdInterview.experience_level,
                    "projectExperience": createdInterview.project_experience,
                    "academicBackground": createdInterview.academic_background,
                    "techStack": createdInterview.tech_stack
                }

                print()
                print(f"payload: {payload}")
                print()
                response = HttpClient.postToAI("/interview/question/generate", payload)
                print(f"FastAPI Response: {response}") # 이게 출력되면 FastAPI로 정보 보내기 성공

                if not response:
                    raise Exception("FastAPI 질문 생성 실패")

                question = response["question"]
                questionId = self.interviewService.saveQuestion(createdInterview.id, question)
                # 방금 생성된 면접 세션(createdInterview.id)에 질문 하나를 DB에 저장하고, 그 질문의 ID(questionId)를 반환받는 코드

                if questionId is None:
                    raise Exception("질문 저장 실패")

            return JsonResponse({
                "message": "면접 정보가 추가되었습니다.",
                "interviewId": createdInterview.id,
                "questionId": questionId,
                "question": question,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ 면접 생성 트랜잭션 실패: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 첫질문 꼬리질문
    @action(detail=False, methods=["post"])
    def requestFollowUpQuestion(self, request):
        postRequest = request.data
        jobCategory = postRequest.get("jobCategory")
        experienceLevel = postRequest.get("experienceLevel")
        academicBackground = postRequest.get("academicBackground")
        projectExperience = postRequest.get("projectExperience")
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")
        companyName = postRequest.get("companyName")

        request_data = {
            'jobCategory': jobCategory,
            'experienceLevel': experienceLevel,
            'academicBackground': academicBackground,
            'userToken': userToken,
            'interviewId': interviewId,
            'questionId': questionId,
            'answerText': answerText,
            'projectExperience': projectExperience,
            'companyName': companyName
        }
        print(f"[요청 데이터] {request_data}")
        if not userToken or not interviewId or not questionId or not answerText or not jobCategory or not experienceLevel or not academicBackground or not projectExperience or not companyName:
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText, jobCategory, experienceLevel, academicBackground, projectExperience, interviewCompany 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)
        print("팔로우업까진 옴. 시작?")
        try:
            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId,
                "answerText": answerText,
                "topic": jobCategory,
                "experienceLevel": experienceLevel,
                "academicBackground": academicBackground,
                "projectExperience": projectExperience,
                "companyName": companyName
            }
            print(f"payload: {payload}")

            response = HttpClient.postToAI("/interview/question/first-followup-generate", payload)
            print(f"[FastAPI]First Follow-up response: {response}")

            if not response:
                raise Exception("FastAPI 질문 생성 실패")
            questions = response.get("questions", [])
            if questions:
                question_text = questions[0] if isinstance(questions, list) and questions else questions
                saved_question_id = self.interviewService.saveQuestion(interviewId, question_text)
                print(f"✅ 심화질문 저장 완료. 질문 ID: {saved_question_id}")
            return JsonResponse(response, status=200)

        except Exception as e:
            print(f"[Error] requestFollowUpQuestion: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    def requestProjectCreateInterview(self, request):
        postRequest = request.data
        print(f"postRequest: {postRequest}")

        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        jobCategory = postRequest.get("jobCategory")
        experienceLevel = postRequest.get("experienceLevel")
        projectExperience = postRequest.get("projectExperience")
        academicBackground = postRequest.get("academicBackground")
        techStack = postRequest.get("interviewTechStack")
        companyName = postRequest.get("companyName")
        questionId = postRequest.get("questionId")
        print(f"techStack:{techStack}")

        # 두번째 질문
        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        if (jobCategory is None or experienceLevel is None or projectExperience is None or academicBackground is None ):
            return JsonResponse({"error": "필수 항목 누락", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        print(f"userToken 획득")

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"accountId 찾기: {accountId}")

            with transaction.atomic():  # ✅ 트랜잭션 블록 시작
                createdInterview = self.interviewService.createInterview(
                    accountId, jobCategory, experienceLevel,projectExperience, academicBackground, techStack, companyName  # 지금 accountId가 안옴
                )
                print(f"createdInterview : {createdInterview}")

                payload = {   # 이 정보만 FastAPI로 전달
                    "userToken": userToken,
                    "interviewId": interviewId,
                    #"topic": createdInterview.topic,
                    "questionId": questionId,
                    #"experienceLevel": createdInterview.experience_level,
                    "projectExperience": projectExperience,
                    #"academicBackground": createdInterview.academic_background,
                    #"techStack": createdInterview.tech_stack
                }
                print(f" project: payload {payload}")

                response = HttpClient.postToAI("/interview/question/project-generate", payload)
                print(f"FastAPI Response: {response}") # 이게 출력되면 FastAPI로 정보 보내기 성공

                if not response:
                    raise Exception("FastAPI 질문 생성 실패")

                question = response["question"]
                question_text = question[0]
                flowQuestionId = response["questionId"]
                questionId = self.interviewService.saveQuestion(interviewId, question_text)
                # 방금 생성된 면접 세션(createdInterview.id)에 질문 하나를 DB에 저장하고, 그 질문의 ID(questionId)를 반환받는 코드

                if questionId is None:
                    raise Exception("질문 저장 실패")

            return JsonResponse({
                "message": "면접 정보가 추가되었습니다.",
                "interviewId": interviewId,
                "questionId": flowQuestionId,
                "question": question,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ 면접 생성 트랜잭션 실패: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"])
    def requestProjectFollowUpQuestion(self, request):
        postRequest = request.data
        jobCategory = postRequest.get("jobCategory")
        projectExperience = postRequest.get("projectExperience")
        #experienceLevel = postRequest.get("experienceLevel")
        #academicBackground = postRequest.get("academicBackground")
        techStack = postRequest.get("interviewTechStack")
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")
        companyName = postRequest.get("companyName")

        print(
            f"[요청 데이터] { {'jobCategory': jobCategory, 'techStack':techStack, 'userToken': userToken, 'interviewId': interviewId, 'questionId': questionId, 'answerText': answerText, 'projectExperience': projectExperience, 'companyName': companyName} }")

        if not userToken or not interviewId or not questionId or not techStack or not answerText or not jobCategory or not projectExperience or not companyName:
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText, jobCategory, projectExperience 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId,
                "answerText": answerText,
                "topic": jobCategory,
                "techStack": techStack,
                "projectExperience": projectExperience,
                "companyName": companyName
            }
            print(f"payload: {payload}")

            response = HttpClient.postToAI("/interview/question/project-followup-generate", payload)
            print(f"[FastAPI]First Follow-up response: {response}")

            if not response:
                raise Exception("FastAPI 질문 생성 실패")
            questions = response.get("questions", [])
            if questions:
                question_text = questions[0]
                saved_question_id = self.interviewService.saveQuestion(interviewId, question_text)
                print(f"✅ 저장된 프로젝트 심화질문 ID: {saved_question_id}")
            return JsonResponse(response, status=200)

        except Exception as e:
            print(f"[Error] requestFollowUpQuestion: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    @action(detail=False, methods=["post"])
    def requestTechFollowUpQuestion(self, request):
        postRequest = request.data
        # jobCategory = postRequest.get("jobCategory")
        # projectExperience = postRequest.get("projectExperience")
        # experienceLevel = postRequest.get("experienceLevel")
        # academicBackground = postRequest.get("academicBackground")
        techStack = postRequest.get("interviewTechStack")
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")
        # companyName = postRequest.get("companyName")

        if not userToken or not interviewId or not questionId or not techStack or not answerText :
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText, jobCategory, projectExperience 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId,
                "answerText": answerText,
                # "topic": jobCategory,
                "techStack": techStack,
                # "academicBackground": academicBackground,
                # "experienceLevel": experienceLevel,
                # "projectExperience": projectExperience,
                # "companyName": companyName
            }
            print(f"payload: {payload}")

            response = HttpClient.postToAI("/interview/question/tech-followup-generate", payload)
            print(f"[FastAPI]Tech Follow-up response: {response}")

            if not response:
                raise Exception("FastAPI 질문 생성 실패")
            questions = response.get("questions", [])
            if questions:
                question_text = questions[0]
                saved_question_id = self.interviewService.saveQuestion(interviewId, question_text)
                print(f"✅ 저장된 프로젝트 심화질문 ID: {saved_question_id}")
            return JsonResponse(response, status=200)

        except Exception as e:
            print(f"[Error] requestFollowUpQuestion: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    # def requestTechCreateInterview(self, request):
    #     postRequest = request.data
    #     print(f"postRequest: {postRequest}")
    #
    #     userToken = postRequest.get("userToken")
    #     interviewId = postRequest.get("interviewId")
    #     jobCategory = postRequest.get("jobCategory")
    #     experienceLevel = postRequest.get("experienceLevel")
    #     projectExperience = postRequest.get("projectExperience")
    #     academicBackground = postRequest.get("academicBackground")
    #     techStack = postRequest.get("interviewTechStack")
    #     companyName = postRequest.get("companyName")
    #     questionId = postRequest.get("questionId")
    #     print(f"techStack:{techStack}")
    #
    #     # 세번째 질문
    #     if not userToken:
    #         return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)
    #     if (jobCategory is None or experienceLevel is None or projectExperience is None or academicBackground is None ):
    #         return JsonResponse({"error": "필수 항목 누락", "success": False},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #
    #     print(f"userToken 획득")
    #
    #     try:
    #         accountId = self.redisCacheService.getValueByKey(userToken)
    #         print(f"accountId 찾기: {accountId}")
    #
    #         with transaction.atomic():  # ✅ 트랜잭션 블록 시작
    #             createdInterview = self.interviewService.createInterview(
    #                 accountId, jobCategory, experienceLevel,projectExperience, academicBackground, techStack, companyName  # 지금 accountId가 안옴
    #             )
    #             print(f"createdInterview : {createdInterview}")
    #
    #             payload = {   # 이 정보만 FastAPI로 전달
    #                 "userToken": userToken,
    #                 "interviewId": interviewId,
    #                 "topic": createdInterview.topic,
    #                 "questionId": questionId,
    #                 #"experienceLevel": createdInterview.experience_level,
    #                 "projectExperience": projectExperience,
    #                 "academicBackground": createdInterview.academic_background,
    #                 "techStack": createdInterview.tech_stack
    #             }
    #             print(f" tech: payload {payload}")
    #
    #             response = HttpClient.postToAI("/interview/question/tech-start", payload)
    #             print(f"FastAPI Response: {response}") # 이게 출력되면 FastAPI로 정보 보내기 성공
    #
    #             if not response:
    #                 raise Exception("FastAPI 질문 생성 실패")
    #
    #             question = response["question"]
    #             question_text = question[0]
    #             flowQuestionId = response["questionId"]
    #             questionId = self.interviewService.saveQuestion(interviewId, question_text)
    #             # 방금 생성된 면접 세션(createdInterview.id)에 질문 하나를 DB에 저장하고, 그 질문의 ID(questionId)를 반환받는 코드
    #
    #             if questionId is None:
    #                 raise Exception("질문 저장 실패")
    #
    #         return JsonResponse({
    #             "message": "면접 정보가 추가되었습니다.",
    #             "interviewId": interviewId,
    #             "questionId": flowQuestionId,
    #             "question": question,
    #             "success": True
    #         }, status=status.HTTP_200_OK)
    #
    #     except Exception as e:
    #         print(f"❌ 면접 생성 트랜잭션 실패: {e}")
    #         return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

