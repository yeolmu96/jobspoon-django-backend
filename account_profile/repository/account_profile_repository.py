from abc import ABC, abstractmethod


class AccountProfileRepository(ABC):

    @abstractmethod
    def save(self, account, nickname, gender, birthyear, age_range):
        pass

    @abstractmethod
    def saveAdmin(self, account, email):
        pass

    @abstractmethod
    def findByAccount(self, account):
        pass

    @abstractmethod
    def findByEmail(self, accountId):
        pass

    @abstractmethod
    def findByRoleType(self, roleType):
        pass

    @abstractmethod
    def findByNickname(self, accountId):
        pass

    @abstractmethod
    def findByGender(self, accountId):
        pass

    @abstractmethod
    def findByBirthyear(self, accountId):
        pass
