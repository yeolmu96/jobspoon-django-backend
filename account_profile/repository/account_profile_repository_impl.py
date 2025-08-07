from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account_profile.entity.account_profile import AccountProfile
from account_profile.entity.admin_profile import AdminProfile
from account_profile.repository.account_profile_repository import AccountProfileRepository


class AccountProfileRepositoryImpl(AccountProfileRepository):
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

    def save(self, account, nickname, gender, birthyear, age_range):
        print("여긴가")
        print(f"accountProfile이: {gender}, {birthyear}, {age_range}")

        gender = gender if gender != '' else 'None'
        birthyear = birthyear if birthyear != '' else '0000'
        age_range = age_range if age_range != '' else 'None'

        original_nickname = nickname or "temporary"
        new_nickname = original_nickname
        count = 1

        # 사전에 nickname 존재 여부 확인
        while AccountProfile.objects.filter(nickname=new_nickname).exists():
            new_nickname = f"{original_nickname}_{count}"
            count += 1
            print(f"Nickname 중복 발견, 새 닉네임 시도: {new_nickname}")

        # 중복 없으면 저장
        accountProfile = AccountProfile.objects.create(
            account=account,
            nickname=new_nickname,
            gender=gender,
            birthyear=birthyear,
            age_range=age_range
        )
        print(f"accountProfile 생성 성공: {gender}, {birthyear}, {age_range}")

        return accountProfile

    def saveAdmin(self, account, email):
        print("다음으로 여기")

        adminProfile = AdminProfile.objects.create(
            account=account,
            email=email
        )
        print(f"accountProfile 생성 성공: {email}")

        return adminProfile


    def findByAccount(self, account): # 객체 하나로 전체 정보 가져오기
        try:
            # 주어진 Account 객체에 해당하는 AccountProfile을 조회
            return AccountProfile.objects.get(account=account)
        except AccountProfile.DoesNotExist:
            # 만약 해당하는 AccountProfile이 없으면 None을 반환
            return None

    #email 찾기
    def findByEmail(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.email
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    #roletype 찾기
    def findByRoleType(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.roleType_id
        except Exception as e:
            print(f"Unexpected error, findByRoleType() : {str(e)}")
            return None

    #nickname 찾기
    def findByNickname(self, accountId):
        try:
            profileNickname=AccountProfile.objects.get(account_id = accountId)
            return profileNickname.nickname
        except ObjectDoesNotExist:
            print(f'No Account found for accountId: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByNickname() : {str(e)}")
            return None

    #gender 찾기
    def findByGender(self, accountId):
        try:
            profileGender = AccountProfile.objects.get(account_id=accountId)
            return profileGender.gender
        except ObjectDoesNotExist:
            print(f'No Account found for accountId: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByGender() : {str(e)}")
            return None

    #birthYar 찾기
    def findByBirthyear(self, accountId):
        try:
            profileBirth = AccountProfile.objects.get(account_id=accountId)
            return profileBirth.birthyear
        except ObjectDoesNotExist:
            print(f'No Account found for birthyear: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByBirthyear() : {str(e)}")
            return None
