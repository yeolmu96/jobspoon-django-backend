from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kakao_oauth.controller.kakao_oauth_controller import KakaoOauthController

router = DefaultRouter()
router.register(r"kakao-oauth", KakaoOauthController, basename='kakao-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         KakaoOauthController.as_view({ 'get': 'requestKakaoOauthLink' }),
         name='Kakao Oauth 링크 요청'),
    path('redirect-access-token',
         KakaoOauthController.as_view({ 'post': 'requestAccessToken' }),
         name='Kakao Access Token 요청'),
    path('request-user-token',
         KakaoOauthController.as_view({ 'post': 'requestUserToken' }),
         name='User Token 요청'),
    path('request-withdraw-url',
         KakaoOauthController.as_view({'post': 'requestKakaoWithdrawLink'}),
         name='Kakao 연결 끊기 요청'),
]