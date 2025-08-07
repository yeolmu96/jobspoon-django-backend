from abc import ABC, abstractmethod


class AccountRepository(ABC):

    @abstractmethod
    def save(self, email, loginType):
        pass

    @abstractmethod
    def saveAdmin(self, email, loginType):
        pass

    @abstractmethod
    def saveWithdralInfo(self, accountId):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def saveWithdrawAt(self, time):
        pass

    @abstractmethod
    def saveWithdrawEnd(self, time):
        pass

    @abstractmethod
    def deleteAccount(self, accountId: int) -> bool:
        pass

    @abstractmethod
    def countEmail(self, guest_email):
        pass
