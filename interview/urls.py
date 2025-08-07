from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview.controller.interview_controller import InterviewController

router = DefaultRouter()
router.register(r"interview", InterviewController, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
    path('create',
         InterviewController.as_view({ 'post': 'requestCreateInterview' }),
         name='인터뷰 질문 생성 및 추가'),
    path('list',
         InterviewController.as_view({ 'post': 'requestListInterview' }),
         name='인터뷰 리스트'),
    path('remove',
         InterviewController.as_view({ 'post': 'requestRemoveInterview' }),
         name='인터뷰 제거'),
    path('user-answer',
         InterviewController.as_view({ 'post': 'requestCreateAnswer' }),
         name='인터뷰 사용자 답변 등록'),
    path('followup',
         InterviewController.as_view({'post': 'requestFollowUpQuestion'}),
         name='꼬리 질문 요청'),
    path('project-create',
         InterviewController.as_view({'post': 'requestProjectCreateInterview'}),
         name='Project 인터뷰 질문 생성 및 추가'),
    path('project-followup',
         InterviewController.as_view({'post': 'requestProjectFollowUpQuestion'}),
         name='Project 꼬리 질문 요청'),
    path('tech-followup',
         InterviewController.as_view({'post': 'requestTechFollowUpQuestion'}),
         name='Tech 질문 요청'),
]
