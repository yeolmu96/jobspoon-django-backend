from abc import ABC, abstractmethod


class KakaoOauthService(ABC):

    @abstractmethod
    def requestKakaoOauthLink(self):
        pass

    @abstractmethod
    def requestAccessToken(self, code):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass

    @abstractmethod
    def requestKakaoWithdrawLink(self):
        pass
