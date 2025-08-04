from django.urls import path, include
from rest_framework.routers import DefaultRouter

from google_oauth.controller.google_oauth_controller import GoogleOauthController

router = DefaultRouter()
router.register(r"google-oauth", GoogleOauthController, basename='google-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         GoogleOauthController.as_view({ 'get': 'requestGoogleOauthLink' }),
         name='Google Oauth 링크 요청'),
    path('redirect-access-token',
         GoogleOauthController.as_view({ 'post': 'requestAccessToken' }),
         name='Google Access Token 요청'),
    path('request-user-token',
         GoogleOauthController.as_view({ 'post': 'requestUserToken' }),
         name='User Token 요청'),
    path('request-withdraw-url',
         GoogleOauthController.as_view({'post': 'requestGoogleWithdrawLink'}),
         name='Google 연결 끊기 요청'),
]