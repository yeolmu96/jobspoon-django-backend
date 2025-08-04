from abc import ABC, abstractmethod


class GuestOauthRepository(ABC):

    @abstractmethod
    def getUserInfo(self, accessToken):
        pass
