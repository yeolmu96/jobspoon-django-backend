from rest_framework import viewsets, status
from django.http import JsonResponse
from interview_question_data.service.interview_question_service_impl import InterviewQuestionServiceImpl


# 질문 관련 HTTP 요청을 처리하는 컨트롤러
class InterviewQuestionController(viewsets.ViewSet):
    service = InterviewQuestionServiceImpl.getInstance()

    def requstSaveBulkInterviewQuestion(self, request):
        # FastAPI에서 생성한 질문 리스트 저장
        interview_id = request.data.get("interviewId")
        question_list = request.data.get("questions")

        if not interview_id or not isinstance(question_list, list):
            return JsonResponse({"error": "interviewId와 questions 리스트가 필요합니다."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            saved = self.service.saveQuestions(interview_id, question_list)
            return JsonResponse({
                "success": True,
                "savedCount": len(saved),  # 실제 저장된 개수
                "skippedCount": len(question_list) - len(saved),  # 중복 등으로 건너뛴 개수
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestListInterviewQuestion(self, request):
        # 특정 인터뷰 ID로 질문 목록 조회
        interview_id = request.query_params.get("interviewId")
        if not interview_id:
            return JsonResponse({"error": "interviewId가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            questions = self.service.getQuestions(interview_id)
            data = [{"id": q.id, "questionText": q.question_text} for q in questions]
            return JsonResponse({"success": True, "questions": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_all_questions(self, request):
        questions = InterviewQuestionServiceImpl.list_questions()
        data = [
            {
                'question': q.question,
                'category': q.category,
                'source': q.source
            } for q in questions
        ]
        return JsonResponse(data, safe=False)