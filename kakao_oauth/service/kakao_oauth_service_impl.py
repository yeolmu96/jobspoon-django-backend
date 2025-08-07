from kakao_oauth.repository.kakao_oauth_repository_impl import KakaoOauthRepositoryImpl
from kakao_oauth.service.kakao_oauth_service import KakaoOauthService


class KakaoOauthServiceImpl(KakaoOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__kakaoOauthRepository = KakaoOauthRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestKakaoOauthLink(self):
        return self.__kakaoOauthRepository.getOauthLink()

    def requestAccessToken(self, code):
        return self.__kakaoOauthRepository.getAccessToken(code)

    def requestUserInfo(self, accessToken):
        print(f" 오류 안남 ")
        return self.__kakaoOauthRepository.getUserInfo(accessToken)

    def requestKakaoWithdrawLink(self, accessToken):
        return self.__kakaoOauthRepository.getWithdrawLink(accessToken)
