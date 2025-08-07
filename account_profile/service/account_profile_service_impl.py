from django.core.exceptions import ObjectDoesNotExist

from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from account_profile.service.account_profile_service import AccountProfileService


class AccountProfileServiceImpl(AccountProfileService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createAccountProfile(self, accountId, nickname, gender, birthyear, age_range):
        print("profile 진입")
        account = self.__accountRepository.findById(accountId)

        original_nickname = nickname or "temporary"
        new_nickname = original_nickname
        count = 1

        while True:
            from MySQLdb import IntegrityError
            try:
                savedAccountProfile = self.__accountProfileRepository.save(
                    account,
                    new_nickname,
                    gender or '',
                    birthyear or '',
                    age_range or ''
                )
                break  # 저장 성공하면 루프 탈출
            except IntegrityError:
                # 닉네임 중복일 경우 새로운 닉네임 생성
                new_nickname = f"{original_nickname}_{count}"
                count += 1
                print(f"닉네임 중복 발생, 새로운 닉네임 시도: {new_nickname}")


        # savedAccountProfile = self.__accountProfileRepository.save(
        #     account,
        #     nickname or "temporary",
        #     gender or '',
        #     birthyear or '',
        #     age_range or ''
        # )

        # if not nickname:
        #     nickname = "temporary"
        # if not gender:
        #     gender = ''
        # if not birthyear:
        #     birthyear = ''
        # if not age_range:
        #     age_range = ''
        #
        # account = self.__accountRepository.findById(accountId)
        # savedAccountProfile = self.__accountProfileRepository.save(account, nickname, gender, birthyear, age_range)
        if savedAccountProfile is not None:
            print(f"Profile 생성 성공: {savedAccountProfile}")
            return True

        print("Profile 생성 실패")
        return False

    def createAdminProfile(self, accountId, email):
        print("adminProfile 진입")

        account = self.__accountRepository.findById(accountId)
        savedAdminProfile = self.__accountProfileRepository.saveAdmin(
            account,
            email,
        )
        if savedAdminProfile is not None:
            print(f"Profile 생성 성공: {savedAdminProfile}")
            return True

        print("adminProfile 생성 실패")
        return False

        # MyPage에서 정보 검색

    def findEmail(self, accountId):  # 얘는 account에서 참조해서 가져와야함
        try:
            accountProfile = self.__accountProfileRepository.findByEmail(accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def findRoleType(self, accountId):  # 얘는 account에서 참조해서 가져와야함
        try:
            accountProfile = self.__accountProfileRepository.findByRoleType(account_id=accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def findNickname(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByNickname(accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def findGender(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByGender(accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

        except ObjectDoesNotExist:
            return None

    def findBirthyear(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByBirthyear(accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def updateAccountProfileIfExists(self, accountId, nickname, gender, birthyear, age_range):
        account = self.__accountRepository.findById(accountId)
        try:
            profile = self.__accountProfileRepository.findByAccount(account)
            if profile:
                if nickname:
                    profile.nickname = nickname
                if gender:
                    profile.gender = gender
                if birthyear:
                    profile.birthyear = birthyear
                if age_range:
                    profile.age_range = age_range
                profile.save()
                print(f"기존 프로필 갱신 완료: {profile}")
                return True
            else:
                # 없으면 생성
                return self.createAccountProfile(accountId, nickname, gender, birthyear, age_range)
        except Exception as e:
            print(f"프로필 갱신 중 오류 발생: {str(e)}")
            return False
