from django.urls import path, include
from rest_framework.routers import DefaultRouter

from github_authentication.controller.github_oauth_controller import GithubOauthController

router = DefaultRouter()
router.register(r"github-oauth", GithubOauthController, basename='github-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         GithubOauthController.as_view({ 'get': 'requestGithubOauthLink' }),
         name='Github Oauth 링크 요청'),
    path('redirect-access-token',
         GithubOauthController.as_view({ 'post': 'requestAccessToken' }),
         name='Github Access Token 요청'),
    path('request-admin-code-validation',
         GithubOauthController.as_view({ 'post': 'requestAdminCodeValidation' }),
         name='관리자 확인 코드'),
]