from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta

from account.entity.withdrawal_membership import WithdrawalMembership
from account.repository.account_repository_impl import AccountRepositoryImpl
from account.service.account_service import AccountService


class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # DB 생성
    def createAccount(self, email, loginType):
        return self.__accountRepository.save(email, loginType)

    def createAdminAccount(self, email, loginType):
        return self.__accountRepository.saveAdmin(email, loginType)

    def createWithdrawalAccount(self, accountId):
        return self.__accountRepository.saveWithdralInfo(accountId)


    # 이메일 중복확인
    def checkEmailDuplication(self, email):
        try:
            return self.__accountRepository.findByEmail(email)

        except ObjectDoesNotExist:
            return None

    # MyPage 회원정보 수정칸
    def findEmail(self, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            if account:
                return account.getEmail()  # account 객체에서 이메일 반환
            return None  # 이메일이 없으면 None 반환

        except ObjectDoesNotExist:
            return None

    def createWithdrawAt(self, accountId,time):
        return self.__accountRepository.saveWithdrawAt(accountId,time)


    def createWithdrawEnd(self, accountId,time):
        return self.__accountRepository.saveWithdrawEnd(accountId,time)

    # 회원 탈퇴
    def withdraw(self, accountId: int) -> bool:
        return self.__accountRepository.deleteAccount(accountId)

    #게스트 회원가입
    def createGuestAccount(self,new_guest_email,loginType):
        return self.__accountRepository.save(new_guest_email,loginType)

    #게스트 이메일 수 카운트
    def countEmail(self, guest_email):
        return self.__accountRepository.countEmail(guest_email)