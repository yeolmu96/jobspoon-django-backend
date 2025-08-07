import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from google_oauth.serializers.google_oauth_access_token_serializer import GoogleOauthAccessTokenSerializer
from google_oauth.service.google_oauth_service_impl import GoogleOauthServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class GoogleOauthController(viewsets.ViewSet):
    googleOauthService = GoogleOauthServiceImpl.getInstance()
    redisService = RedisCacheServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()

    def get_account(self):
        from account_profile.entity.account_profile import AccountProfile
        return AccountProfile

    def requestGoogleOauthLink(self, request):
        url = self.googleOauthService.requestGoogleOauthLink()

        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        print("google requestAccessToken 진입")
        serializer = GoogleOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        print(f"code: {code}")

        try:
            print("google requestAccessToken try: 진입")
            tokenResponse = self.googleOauthService.requestGoogleAccessToken(code)
            accessToken = tokenResponse['access_token']
            print(f"accessToken: {accessToken}")

            with transaction.atomic():
                userInfo = self.googleOauthService.requestUserInfo(accessToken)
                user_id = userInfo.get('sub', '') # 사용자 ID
                #nickname = userInfo.get('properties', {}).get('nickname', '') # 닉네임
                nickname = userInfo.get('name','')
                email = userInfo.get('email', '') #.get('email', '') # 이메일
                gender = userInfo.get('gender', None)  # 성별별
                age_range = userInfo.get('age_range', None) # 연령대
                birthyear = userInfo.get('birthyear', None) # 출생연도
                loginType = 'GOOGLE'
                # 정보 출력 (디버깅용)
                print(f"user_id: {user_id}, email: {email}, nickname: {nickname}")
                print(f"gender: {gender}, age_range: {age_range}, birthyear: {birthyear}")

                # 이메일 형식 확인
                account = self.accountService.checkEmailDuplication(email)
                print(f"account: {account}")

                if account is None:
                    account = self.accountService.createAccount(email, loginType)
                    print(f"accountProfile: {account}")
                    accountProfile = self.accountProfileService.createAccountProfile(
                        account.getId(), nickname, gender, birthyear, age_range
                    )
                    print(f"accountProfile: {accountProfile}")
                else:
                    # 이미 있는 사용자라도 profile 정보를 최신화 (Google은 불완전할 수 있음)
                    accountProfile = self.accountProfileService.updateAccountProfileIfExists(
                        account.getId(), nickname, gender, birthyear, age_range
                    )
                    print(f"accountProfile: {accountProfile}")

                # account = self.accountService.checkEmailDuplication(email)
                # print(f"account: {account}")

                userToken = self.__createUserTokenWithAccessToken(account, accessToken)
                print(f"userToken: {userToken}")

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            import traceback
            print("[Google OAuth Error]", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

        #     if account is None:
        #         account = self.accountService.createAccount(email)
        #         print(f"account: {account}")

        #         accountProfile = self.accountProfileService.createAccountProfile(
        #             account.getId(), nickname
        #         )
        #         print(f"accountProfile: {accountProfile}")

        #     userToken = self.__createUserTokenWithAccessToken(account, accessToken)
        #     print(f"userToken: {userToken}")

        #     return JsonResponse({'userToken': userToken})

        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=500)


    def requestUserToken(self, request):
        global account
        access_token = request.data.get('access_token')  # 클라이언트에서 받은 access_token
        user_id = request.data.get('user_id')# 클라이언트에서 받은 id
        email = request.data.get('email')  # 클라이언트에서 받은 email
        nickname = request.data.get('nickname')  # 클라이언트에서 받은 nickname
        gender = request.data.get('gender', '')  # 클라이언트에서 받은 성별
        age_range = request.data.get('age_range', '')  # 클라이언트에서 받은 연령대
        birthyear = request.data.get('birthyear', '')  # 클라이언트에서 받은 출생연도
        loginType = 'GOOGLE'
        print(f"{request.data}")

        if not access_token:
            return JsonResponse({'error': 'Access token is required'}, status=400)

        if not user_id or not email or not nickname :
            return JsonResponse({'error': 'All user information (ID, email, nickname, gender, age_range, birthyear) is required'}, status=400)

        try:
            # 이메일을 기반으로 계정을 찾거나 새로 생성합니다.
            print('acquire data!')
            account = self.accountService.checkEmailDuplication(email)
            print(f'account: {account}')

            if account is None:
                print("There are no account!")
                account = self.accountService.createAccount(email, loginType)
                accountProfile = self.accountProfileService.createAccountProfile(
                    account.getId(), nickname, gender, birthyear, age_range
                )
                print(f"accountProfile: {accountProfile}")
            else:
                # 이미 있는 사용자라도 profile 정보를 최신화 (Google은 불완전할 수 있음)
                accountProfile = self.accountProfileService.updateAccountProfileIfExists(
                    account.getId(), nickname, gender, birthyear, age_range
                )
                print(f"accountProfile: {accountProfile}")

            print("ready to create userToken")
            # 사용자 토큰 생성 및 Redis에 저장
            userToken = self.__createUserTokenWithAccessToken(account, access_token)

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __createUserTokenWithAccessToken(self, account, accessToken):
        try:
            userToken = str(uuid.uuid4())
            self.redisService.storeKeyValue(account.getId(), accessToken)
            self.redisService.storeKeyValue(userToken, account.getId())

            if not account or not account.getId():
                raise ValueError("Invalid account ID")

            return userToken

        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')

    def requestGoogleWithdrawLink(self, request):
        print("requestGoogleWithdrawLink 진입")

        userToken = request.headers.get("Authorization")
        userToken = userToken.replace("Bearer ", "")
        if not userToken:
            return JsonResponse({"error": "Authorization 헤더가 필요합니다."}, status=400)

        accountId = self.redisService.getValueByKey(userToken)
        if not accountId:
            return JsonResponse({"error": "유효하지 않은 userToken입니다."}, status=400)

        accessToken = self.redisService.getValueByKey(accountId)
        if not accessToken:
            return JsonResponse({"error": "AccessToken을 찾을 수 없습니다."}, status=400)

        # 여기서 바로 Service 호출
        result = self.googleOauthService.requestGoogleWithdrawLink(accessToken)
        print(f"탈퇴 결과 result: {result}")

        return JsonResponse(result, status=HTTP_200_OK)