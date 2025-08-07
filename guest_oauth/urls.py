from django.urls import path, include
from rest_framework.routers import DefaultRouter

from guest_oauth.controller.guest_oauth_controller import GuestOauthController

router = DefaultRouter()
router.register(r"guest-oauth", GuestOauthController, basename='guest-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         GuestOauthController.as_view({ 'post': 'requestGuestSignIn' }),
         name='Google Oauth 링크 요청'),
    path('request-user-token',
         GuestOauthController.as_view({ 'post': 'requestUserToken' }),
         name='User Token 요청'),

]