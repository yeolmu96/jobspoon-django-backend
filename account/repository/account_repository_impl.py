from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account.entity.account_login_type import AccountLoginType
from account.entity.account import Account
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from account.entity.withdrawal_membership import WithdrawalMembership
from account.repository.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def save(self, email, loginType):
        print(f"email: {email}")
        defaultRoleType = AccountRoleType.objects.filter(roleType=RoleType.NORMAL).first()
        loginTypeInstance, created = AccountLoginType.objects.get_or_create(loginType=loginType)

        # 만약 기본 역할이 없다면, 새로 생성
        if not defaultRoleType:
            defaultRoleType = AccountRoleType(roleType=RoleType.NORMAL)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType: {defaultRoleType}")

        print(f"defaultRoleType: {defaultRoleType}")

        try:
            account = Account.objects.create(

                email=email,
                loginType=loginTypeInstance,
                roleType=defaultRoleType,
            )
            print("완료")
            return account

        except IntegrityError as e:

            print(
                f"email={email}, roleType={defaultRoleType}, loginType={loginType}")

            print(f"에러 내용: {e}")

            return None
            # raise IntegrityError(f"Nickname '{nickname}' 이미 존재함.")

    def saveAdmin(self, email, loginType):
        print(f"email: {email}")
        defaultRoleType = AccountRoleType.objects.filter(roleType=RoleType.ADMIN).first()
        loginTypeInstance, created = AccountLoginType.objects.get_or_create(loginType=loginType)
        print(f"defaultRoleType: {defaultRoleType}")

        # 만약 기본 역할이 없다면, 새로 생성
        if not defaultRoleType:
            print(f"defaultRoleType: {defaultRoleType}")
            defaultRoleType = AccountRoleType(roleType=RoleType.ADMIN)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType: {defaultRoleType}")

        print(f"defaultRoleType: {defaultRoleType}")
        print(f"loginType: {loginTypeInstance}")

        account = Account(email=email, roleType=defaultRoleType, loginType=loginTypeInstance)
        print(f"야 찍히냐?")

        account.save()
        print(f"account: {account}")

        return account

    def saveWithdralInfo(self, accountId):
        try:
            print(f"accountId={accountId}")

            # accountId로 새로운 WithdrawalMembership 객체 생성
            withdralMembership = WithdrawalMembership.objects.create(accountId=accountId)

            # 생성된 객체의 필드 값들을 출력하여 확인
            print(
                f"생성된 withdralMembership: ID={withdralMembership.id}, accountId={withdralMembership.accountId}, withdraw_at={withdralMembership.withdraw_at}")

            # 객체를 반환
            return withdralMembership

        except IntegrityError as e:
            print("saveWithdralInfo 에러 뜸")
            print(f"에러 내용: {e}")
            return None  # 에러 발생 시 None 반환



    # DB에서 조회
    def findById(self, accountId):
        print("findById 여기까찌 옴")
        try:
            account = Account.objects.get(id=accountId)
            print(f"Account 찾음: {account}")
            return account
        except ObjectDoesNotExist:
            print(f"Account ID {accountId} 존재하지 않음.")
            return None
    def findByEmail(self, email):
        try:
            print(f"{email}")
            return Account.objects.get(email=email)
        except ObjectDoesNotExist:
            print(f'No account found for email: {email}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


    # 탈퇴시점, 탈퇴시점+3년 DB에 저장
    def saveWithdrawAt(self, accountId,time):
        try:
            withdrawMembership = WithdrawalMembership.objects.get(accountId=accountId)
            withdrawMembership.withdraw_at = time
            withdrawMembership.save()

            print(f"업데이트된 withdrawMembership: {withdrawMembership}")
        except WithdrawalMembership.DoesNotExist:
            print(f"accountId={accountId}인 회원을 찾을 수 없음")

    def saveWithdrawEnd(self, accountId,time):
        try:
            end = time + relativedelta(years=3)
            print(f"saveWithdrawEnd - accountId={accountId}, withdraw_end={end}")

            # 기존의 WithdrawalMembership 객체를 찾아서 업데이트
            withdrawMembership = WithdrawalMembership.objects.get(accountId=accountId)
            withdrawMembership.withdraw_end = end
            withdrawMembership.save()

            print(f"업데이트된 withdrawMembership: {withdrawMembership}")
        except WithdrawalMembership.DoesNotExist:
            print(f"accountId={accountId}인 회원을 찾을 수 없음")



    # 회원 탈퇴시 사용자 정보 삭제
    def deleteAccount(self, accountId: int) -> bool:
        try:
            account = Account.objects.get(id=accountId)
            account.delete()
            print(f"{account}")
            return True
        except Account.DoesNotExist:
            return False
    #게스트 이메일 수
    def countEmail(self, guest_email):
        return Account.objects.filter(email__startswith=guest_email).count()

