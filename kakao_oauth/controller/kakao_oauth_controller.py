import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from kakao_oauth.serializer.kakao_oauth_access_token_serializer import KakaoOauthAccessTokenSerializer
from kakao_oauth.service.kakao_oauth_service_impl import KakaoOauthServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class KakaoOauthController(viewsets.ViewSet):
    kakaoOauthService = KakaoOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def get_account(self):
        from account_profile.entity.account_profile import AccountProfile
        return AccountProfile

    def requestKakaoOauthLink(self, request):
        url = self.kakaoOauthService.requestKakaoOauthLink()

        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestKakaoWithdrawLink(self, request):
        userToken = request.headers.get("Authorization")
        userToken = userToken.replace("Bearer ", "")
        accountId = self.redisCacheService.getValueByKey(userToken)
        accessToken = self.redisCacheService.getValueByKey(accountId)
        if not userToken:
            return JsonResponse({"error": "userToken이 없습니다."}, status=400)

        url = self.kakaoOauthService.requestKakaoWithdrawLink(accessToken)
        print(f"{url}")
        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        serializer = KakaoOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        print(f"code: {code}")

        try:
            tokenResponse = self.kakaoOauthService.requestAccessToken(code)
            print(f"{tokenResponse}")
            accessToken = tokenResponse['access_token']
            print(f"accessToken: {accessToken}")

            with transaction.atomic():
                print(f" 오류 안남 ")
                userInfo = self.kakaoOauthService.requestUserInfo(accessToken)
                print(f"{userInfo}")
                user_id = userInfo.get('id', '')  # 사용자 ID
                nickname = userInfo.get('properties', {}).get('nickname', '')  # 닉네임
                email = userInfo.get('kakao_account', {}).get('email', '')  # 이메일
                gender = userInfo.get('kakao_account', {}).get('gender', '')  # 성별
                age_range = userInfo.get('kakao_account', {}).get('age_range', '')  # 연령대
                birthyear = userInfo.get('kakao_account', {}).get('birthyear', '')  # 출생연도
                loginType='KAKAO'
                # 정보 출력 (디버깅용)
                print(f"user_id: {user_id}, email: {email}, nickname: {nickname}")
                print(f"gender: {gender}, age_range: {age_range}, birthyear: {birthyear}")

                # 이메일 중복 확인
                account = self.accountService.checkEmailDuplication(email)
                print(f"account: {account}")

                if account is None:
                    account = self.accountService.createAccount(email, loginType)
                    print(f"accountProfile: {account}")
                    accountProfile = self.accountProfileService.createAccountProfile(
                        account.getId(), nickname, gender, birthyear, age_range
                    )


                    print(f"accountProfile: {accountProfile}")

                userToken = self.__createUserTokenWithAccessToken(account, accessToken)
                print(f"userToken: {userToken}")

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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

    #def dropRedisTokenForLogout(self, request):
     #   try:
      #      userToken = request.data.get('userToken')
       #     isSuccess = self.redisService.deleteKey(userToken)

#            return Response({'isSuccess': isSuccess}, status=status.HTTP_200_OK)
 #       except Exception as e:
  #          print(f'레디스 토큰 해제 중 에러 발생:', e)
   #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
