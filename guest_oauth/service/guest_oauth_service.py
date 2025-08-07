from abc import ABC, abstractmethod


class GuestOauthService(ABC):

    @abstractmethod
    def countEmail(self):
        pass