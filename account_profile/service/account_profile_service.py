from abc import ABC, abstractmethod


class AccountProfileService(ABC):
    @abstractmethod
    def createAccountProfile(self, accountId, nickname, gender, birthyear, age_range):
        pass

    @abstractmethod
    def createAdminProfile(self, accountId, email):
        pass

    @abstractmethod
    def findEmail(self, accountId):
        pass
    @abstractmethod
    def findRoleType(self, accountId):
        pass
    @abstractmethod
    def findNickname(self, accountId):
        pass
    @abstractmethod
    def findGender(self, accountId):
        pass
    @abstractmethod
    def findBirthyear(self, accountId):
        pass

    @abstractmethod
    def updateAccountProfileIfExists(self, accountId, nickname, gender, birthyear, age_range):
        pass