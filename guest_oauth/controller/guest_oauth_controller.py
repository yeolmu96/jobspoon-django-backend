import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from account.service.account_service_impl import AccountServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class GuestOauthController(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestGuestSignIn(self, request):
        try:
            guest_email = "jobstick"
            guest_dmain = "@jobstick.com"
            loginType = "GUEST"

            #guest 이메일 수 카운트
            guest_count = self.accountService.countEmail(guest_email)

            #새 이메일 생성
            new_guest_email = f"{guest_email}{guest_count+1}{guest_dmain}"

            # 계정 생성
            account = self.accountService.createGuestAccount(new_guest_email,loginType)

            #Redis 발급
            userToken = str(uuid.uuid4())
            self.redisCacheService.storeKeyValue(userToken,account.getId())
            print(f"{userToken}")

            #토큰 반환
            return JsonResponse({'userToken':userToken},status=HTTP_200_OK)

        except Exception as e:
            print(f"게스트 로그인 실패:{e}")
            return JsonResponse({'error':str(e)},status=500)


    #앱에서 사용함
    def requestUserToken(self, request):
        #global accountProfile
        global account

        access_token = request.data.get('access_token')  # 클라이언트에서 받은 access_token
        user_id = request.data.get('user_id')# 클라이언트에서 받은 id
        email = request.data.get('email')  # 클라이언트에서 받은 email
        nickname = request.data.get('nickname')  # 클라이언트에서 받은 nickname
        gender = request.data.get('gender', '')  # 클라이언트에서 받은 성별
        age_range = request.data.get('age_range', '')  # 클라이언트에서 받은 연령대
        birthyear = request.data.get('birthyear', '')  # 클라이언트에서 받은 출생연도
        loginType = 'KAKAO'
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

            print("ready to create userToken")
            # 사용자 토큰 생성 및 Redis에 저장
            userToken = self.__createUserTokenWithAccessToken(account, access_token)

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __createUserTokenWithAccessToken(self, account, accessToken):
        try:
            userToken = str(uuid.uuid4())
            self.redisCacheService.storeKeyValue(account.getId(), accessToken)
            self.redisCacheService.storeKeyValue(userToken, account.getId())

            if not account or not account.getId():
                raise ValueError("Invalid account ID")

            return userToken

        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')