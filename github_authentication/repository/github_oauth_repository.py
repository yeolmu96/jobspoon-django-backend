from abc import ABC, abstractmethod


class GithubOauthRepository(ABC):

    @abstractmethod
    def getOauthLink(self):
        pass

    @abstractmethod
    def getAccessToken(self, githubAuthCode):
        pass

    @abstractmethod
    def getUserInfo(self, accessToken):
        pass

    @abstractmethod
    def getAdminCode(self, adminCode: str) -> bool:
        pass