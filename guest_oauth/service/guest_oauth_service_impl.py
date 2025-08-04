from guest_oauth.repository.guest_oauth_repository_impl import GuestOauthRepositoryImpl
from guest_oauth.service.guest_oauth_service import GuestOauthService


class GuestOauthServiceImpl(GuestOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__guestOauthRepository = GuestOauthRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestUserInfo(self, accessToken):
        return self.__guestOauthRepository.getUserInfo(accessToken)
