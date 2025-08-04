from abc import ABC, abstractmethod


class GoogleOauthRepository(ABC):

    @abstractmethod
    def getOauthLink(self):
        pass

    @abstractmethod
    def getAccessToken(self, code):
        pass

    @abstractmethod
    def getUserInfo(self, accessToken):
        pass
