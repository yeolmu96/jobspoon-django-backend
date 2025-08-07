import requests

from av_db import settings
from guest_oauth.repository.guest_oauth_repository import GuestOauthRepository


class GuestOauthRepositoryImpl(GuestOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        return (
            f"{self.loginUrl}?"
            f"client_id={self.clientId}&"
            f"redirect_uri={self.redirectUri}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile&"
            f"access_type=offline&"
            f"prompt=consent"
        )
    def getAccessToken(self, code):
        accessTokenRequest = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'code': code,
            'client_secret': self.clientSecret
        }

        response = requests.post(self.tokenRequestUri, data=accessTokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        print("getUserInfo 진입")
        headers = {'Authorization': f'Bearer {accessToken}'}
        print(f" accessToken: {accessToken}")
        print(f" headers: {headers}")
        print(f" URL: {self.userInfoRequestUri}")
        response = requests.post(self.userInfoRequestUri, headers=headers)
        print(f"{response}")
        return response.json()

    def getWithdrawLink(self, accessToken):
        """
        구글 OAuth Revoke API 호출
        """
        print("getWithdrawLink() for withdraw - Google")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "token": accessToken
        }

        response = requests.post(self.revokeUrl, params=payload, headers=headers)

        # 응답 확인
        if response.status_code == 200:
            return {"message": "구글 연결 해제 성공"}
        else:
            try:
                return {"error": response.json()}
            except Exception:
                return {"error": response.text}

