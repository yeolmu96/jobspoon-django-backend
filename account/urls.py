from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.account_controller import AccountController

router = DefaultRouter()
router.register(r"account", AccountController, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('request-email',
         AccountController.as_view({ 'post': 'requestEmail' }),
         name='이메일 요청'),
    path('request-withdraw',
         AccountController.as_view({ 'post': 'requestWithdraw' }),
         name='회원 삭제 요청'),
]