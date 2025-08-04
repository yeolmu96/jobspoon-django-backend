from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview_result.controller.interview_result_controller import InterviewResultController

router = DefaultRouter()
router.register(r'interview_result', InterviewResultController, basename='interview_result')
urlpatterns = [
    path('', include(router.urls)),
    path('end-interview', InterviewResultController.as_view({'post': 'requestEndInterview'}), name='end-interview'),
    path('request-interview-summary', InterviewResultController.as_view({'post': 'requestInterviewSummary'}), name='request-interview-summary'),
    path('get-interview-result', InterviewResultController.as_view({'post': 'getInterviewResult'}), name='get-interview-result'),
]
