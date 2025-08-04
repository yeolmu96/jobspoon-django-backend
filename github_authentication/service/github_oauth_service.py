from abc import ABC, abstractmethod


class GithubOauthService(ABC):

    @abstractmethod
    def requestGithubOauthLink(self):
        pass

    @abstractmethod
    def requestAccessToken(self, code):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass

    @abstractmethod
    def validateAdminCode(self, adminCode: str) -> bool:
        pass