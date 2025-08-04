from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review.controller.review_controller import ReviewController

router = DefaultRouter()
router.register(r"review", ReviewController, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('list',
         ReviewController.as_view({ 'get': 'requestReviewList' }),
         name='리뷰 항목 요청'),
    path('upload',
         ReviewController.as_view({ 'post': 'requestUploadReview' }),
         name='리뷰 s3 업로드'),
    path('create',
         ReviewController.as_view({ 'post': 'requestCreateReview' }),
         name='리뷰 등록 요청'),
    path('read/<int:pk>',
         ReviewController.as_view({ 'get': 'requestReadReview' }),
         name='리뷰 읽기 요청'),
    path('update/<int:pk>',
         ReviewController.as_view({ 'put': 'requestUpdateReview' }),
         name='리뷰 수정 요청'),
    path('delete/<int:pk>',
         ReviewController.as_view({'delete': 'requestDeleteReview' }),
         name='리뷰 삭제 요청'),
]