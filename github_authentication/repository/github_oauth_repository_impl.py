import requests

from av_db import settings
from github_authentication.repository.github_oauth_repository import GithubOauthRepository


class GithubOauthRepositoryImpl(GithubOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.GITHUB['LOGIN_URL']
            cls.__instance.clientId = settings.GITHUB['CLIENT_ID']
            cls.__instance.clientSecret = settings.GITHUB['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.GITHUB['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GITHUB['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GITHUB['USER_INFO_REQUEST_URI']
            cls.__instance.adminCode = settings.GITHUB['ADMIN_CODE']
            cls.__instance.scope = settings.GITHUB['SCOPE']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        print("getOauthLink() for Login")

        return (f"{self.loginUrl}?"
                f"client_id={self.clientId}&redirect_uri={self.redirectUri}&scope={self.scope}")

    def getAccessToken(self, githubAuthCode):
        print(f"getAccessToken(): {githubAuthCode}")

        accessTokenRequestForm = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "code": githubAuthCode,
            "redirect_uri": self.redirectUri
        }
        headers = {
            "Accept": "application/json"
        }

        print(f"accessTokenRequestForm: {accessTokenRequestForm}")
        print(f"tokenRequestUri: {self.tokenRequestUri}")

        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForm, headers=headers)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        print(f"headers: {headers}, userInfoRequestUri: {self.userInfoRequestUri}")

        response = requests.get(self.userInfoRequestUri, headers=headers)
        return response.json()

    def getAdminCode(self, adminCode: str) -> bool:
        print(f"Repository validateAdminCode adminCode: {adminCode}")
        print(f"repository validateAdminCode self.adminCode: {self.adminCode}")

        if self.adminCode is None:
            raise ValueError("GITHUB_ADMIN_CODE is not set in settings.")

        return adminCode == self.adminCode