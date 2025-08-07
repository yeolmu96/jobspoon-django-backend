from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account_profile.controller.account_profile_controller import AccountProfileController

router = DefaultRouter()
router.register(r'account_profile', AccountProfileController, basename='account_profile')

urlpatterns = [
    path('', include(router.urls)),
    # 사용자 정의 엔드포인트: POST /account_profile/request-info/
    path('request-info', AccountProfileController.as_view({'post': 'requestInfo'}), name='MyPage 개인정보 요청'),
]
