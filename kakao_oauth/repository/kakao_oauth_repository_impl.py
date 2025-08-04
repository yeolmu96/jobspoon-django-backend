import requests

from av_db import settings
from kakao_oauth.repository.kakao_oauth_repository import KakaoOauthRepository


class KakaoOauthRepositoryImpl(KakaoOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.KAKAO['LOGIN_URL']
            cls.__instance.withdrawUrl = settings.KAKAO['WITHDRAW_URL']
            cls.__instance.clientId = settings.KAKAO['CLIENT_ID']
            cls.__instance.redirectUri = settings.KAKAO['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.KAKAO['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.KAKAO['USER_INFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        print("getOauthLink() for Login")

        return (f"{self.loginUrl}/oauth/authorize?"
                f"client_id={self.clientId}&redirect_uri={self.redirectUri}&response_type=code")



    def getWithdrawLink(self,accessToken):
        print("getWithdrawLink() for withdraw")

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(self.withdrawUrl, headers=headers)

        # 응답 확인
        if response.status_code == 200:
            return response.json()
        else:
            return response.text  # 에러 메시지 반환


    def getAccessToken(self, code):
        accessTokenRequest = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'code': code,
            'client_secret': None
        }

        response = requests.post(self.tokenRequestUri, data=accessTokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.post(self.userInfoRequestUri, headers=headers)
        return response.json()
