import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from github_authentication.service.github_oauth_service_impl import GithubOauthServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class GithubOauthController(viewsets.ViewSet):
    githubOauthService = GithubOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestAdminCodeValidation(self, request):
        try:
            postRequest = request.data
            print(f"postRequest: {postRequest}")

            adminCode = postRequest.get("admin_code")  # 요청에서 관리자 코드 추출
            print(f"controller - validateAdminCode: {adminCode}")

            if not adminCode:
                return JsonResponse({"message": "관리자 코드가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

            isValid = self.githubOauthService.validateAdminCode(adminCode)
            print(f"Validation Result: {isValid}")

            return JsonResponse({"isValid": isValid}, status=HTTP_200_OK)

        except Exception as e:
            print(f"Error in requestAdminCodeValidation: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    def requestGithubOauthLink(self, request):
        url = self.githubOauthService.requestGithubOauthLink()

        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        postRequest = request.data

        code = postRequest.get('code')
        print(f"code: {code}")

        try:
            tokenResponse = self.githubOauthService.requestAccessToken(code)
            accessToken = tokenResponse['access_token']
            print(f"accessToken: {accessToken}")

            with transaction.atomic():
                userInfo = self.githubOauthService.requestUserInfo(accessToken)
                print(f"userInfo: {userInfo}")

                email = userInfo.get('email', '')
                nickname = userInfo.get('login', '')
                loginType = 'GITHUB'
                print(f"email: {email}, nickname: {nickname}")

                account = self.accountService.checkEmailDuplication(email)
                print(f"account: {account}")

                if account is None:
                    account = self.accountService.createAdminAccount(email, loginType)
                    print(f"account: {account}")

                    accountProfile = self.accountProfileService.createAdminProfile(
                        account.getId(), email
                    )
                    print(f"accountProfile: {accountProfile}")

                userToken = self.__createUserTokenWithAccessToken(account, accessToken)
                print(f"userToken: {userToken}")

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __createUserTokenWithAccessToken(self, account, accessToken):
        try:
            userToken = 'gho_' + str(uuid.uuid4())
            self.redisCacheService.storeKeyValue(account.getId(), accessToken)
            self.redisCacheService.storeKeyValue(userToken, account.getId())

            return userToken

        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')