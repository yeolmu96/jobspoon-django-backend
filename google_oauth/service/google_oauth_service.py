from abc import ABC, abstractmethod


class GoogleOauthService(ABC):

    @abstractmethod
    def requestGoogleOauthLink(self):
        pass

    @abstractmethod
    def requestGoogleAccessToken(self, code):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass
