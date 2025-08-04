from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from training_sample.service.training_sample_service_impl import TrainingSampleServiceImpl
from utility.http_client import HttpClient

class TrainingSampleController(viewsets.ViewSet):

    @action(detail=False, methods=["post"])
    def send_to_fastapi(self, request):
        try:
            service = TrainingSampleServiceImpl.getInstance()
            training_data = service.get_training_data()

            if not training_data:
                return Response({
                    "message": "학습 데이터가 존재하지 않습니다.",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)

            payload = {
                "userToken": "training-mode",
                "interviewId": -999,
                "evaluationData": training_data
            }

            response = HttpClient.postToAI("/interview/question/end_interview", payload)

            return Response({
                "message": "학습 샘플 전송 성공",
                "sent": len(training_data),
                "fastapi_response": response,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "FastAPI 전송 실패",
                "error": str(e),
                "success": False
            }, status=status.HTTP_502_BAD_GATEWAY)