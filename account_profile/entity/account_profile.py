# Non-ORM 버전의 AccountProfile 클래스
# Django Model을 상속받지 않고 일반 클래스로 구현

from django.db import connections
from account.entity.account import Account


class AccountProfile:
    """
    Django Model을 상속받지 않고 일반 클래스로 구현한 AccountProfile 클래스
    기존 코드와의 호환성을 위해 동일한 메서드와 속성 유지
    """
    db_table = 'account_profile'  # 테이블 이름 지정
    
    def __init__(self, id=None, account_id=None, nickname=None, gender=None, birthyear=None, age_range=None):
        self.id = id
        self.account_id = account_id
        self._account = None  # 실제 account 객체는 필요할 때만 로드
        self.nickname = nickname
        self.gender = gender
        self.birthyear = birthyear
        self.age_range = age_range
    
    def __str__(self):
        return f"AccountProfile(id={self.id}, account_id={self.account_id}, nickname={self.nickname})"
    
    class Meta:
        # Django ORM과의 호환성을 위해 Meta 클래스 유지
        db_table = 'account_profile'
        app_label = 'account_profile'
    
    @property
    def account(self):
        """
        account 속성에 접근할 때 필요에 따라 Account 객체를 가져옴
        """
        if self._account is None and self.account_id is not None:
            self._account = Account.objects().get(id=self.account_id)
        return self._account
    
    @account.setter
    def account(self, account):
        """
        account 속성 설정 시 account_id도 함께 설정
        """
        self._account = account
        if account is not None:
            self.account_id = account.id
        else:
            self.account_id = None
    
    @staticmethod
    def objects():
        """
        Django ORM의 objects 매니저와 유사한 기능을 제공하는 메서드
        AccountProfile.objects().all(), AccountProfile.objects().filter() 등의 호출을 지원
        """
        return AccountProfileManager()


class AccountProfileManager:
    """
    Django ORM의 Manager와 유사한 기능을 제공하는 클래스
    """
    def __init__(self):
        self.db_connection = 'default'  # settings.py에 정의된 DB 연결 사용
    
    def all(self):
        """
        모든 AccountProfile 객체를 반환
        """
        try:
            profiles = []
            with connections[self.db_connection].cursor() as cursor:
                cursor.execute(
                    "SELECT id, account_id, nickname, gender, birthyear, age_range FROM account_profile"
                )
                rows = cursor.fetchall()
                for row in rows:
                    profile = AccountProfile(
                        id=row[0],
                        account_id=row[1],
                        nickname=row[2],
                        gender=row[3],
                        birthyear=row[4],
                        age_range=row[5]
                    )
                    profiles.append(profile)
            return profiles
        except Exception as e:
            print(f"DB 조회 오류: {e}")
            return []
    
    def get(self, **kwargs):
        """
        조건에 맞는 단일 AccountProfile 객체를 반환
        """
        try:
            conditions = []
            params = []
            for key, value in kwargs.items():
                if key == 'id':
                    conditions.append('id = %s')
                    params.append(value)
                elif key == 'account_id':
                    conditions.append('account_id = %s')
                    params.append(value)
                elif key == 'nickname':
                    conditions.append('nickname = %s')
                    params.append(value)
                # 필요에 따라 더 많은 조건 추가 가능
            
            if not conditions:
                raise ValueError("검색 조건이 지정되지 않았습니다.")
            
            with connections[self.db_connection].cursor() as cursor:
                query = f"SELECT id, account_id, nickname, gender, birthyear, age_range FROM account_profile WHERE {' AND '.join(conditions)}"
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    return AccountProfile(
                        id=row[0],
                        account_id=row[1],
                        nickname=row[2],
                        gender=row[3],
                        birthyear=row[4],
                        age_range=row[5]
                    )
            raise AccountProfile.DoesNotExist(f"조건에 맞는 AccountProfile이 없습니다: {kwargs}")
        except Exception as e:
            if not isinstance(e, AccountProfile.DoesNotExist):
                print(f"DB 조회 오류: {e}")
            raise
    
    def filter(self, **kwargs):
        """
        조건에 맞는 여러 AccountProfile 객체를 반환
        """
        try:
            profiles = []
            conditions = []
            params = []
            
            for key, value in kwargs.items():
                if key == 'id':
                    conditions.append('id = %s')
                    params.append(value)
                elif key == 'account_id':
                    conditions.append('account_id = %s')
                    params.append(value)
                elif key == 'nickname':
                    conditions.append('nickname = %s')
                    params.append(value)
                # 필요에 따라 더 많은 조건 추가 가능
            
            query = "SELECT id, account_id, nickname, gender, birthyear, age_range FROM account_profile"
            if conditions:
                query += f" WHERE {' AND '.join(conditions)}"
            
            with connections[self.db_connection].cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                for row in rows:
                    profile = AccountProfile(
                        id=row[0],
                        account_id=row[1],
                        nickname=row[2],
                        gender=row[3],
                        birthyear=row[4],
                        age_range=row[5]
                    )
                    profiles.append(profile)
            return profiles
        except Exception as e:
            print(f"DB 조회 오류: {e}")
            return []
    
    def create(self, **kwargs):
        """
        새로운 AccountProfile 객체를 생성하고 저장
        """
        try:
            fields = []
            values = []
            placeholders = []
            
            # account 객체를 처리
            if 'account' in kwargs:
                account = kwargs.pop('account')
                fields.append('account_id')
                values.append(account.id)
                placeholders.append('%s')
            elif 'account_id' in kwargs:
                fields.append('account_id')
                values.append(kwargs.pop('account_id'))
                placeholders.append('%s')
            
            # 나머지 필드 처리
            for key, value in kwargs.items():
                if key == 'nickname':
                    fields.append('nickname')
                    values.append(value)
                    placeholders.append('%s')
                elif key == 'gender':
                    fields.append('gender')
                    values.append(value)
                    placeholders.append('%s')
                elif key == 'birthyear':
                    fields.append('birthyear')
                    values.append(value)
                    placeholders.append('%s')
                elif key == 'age_range':
                    fields.append('age_range')
                    values.append(value)
                    placeholders.append('%s')
            
            with connections[self.db_connection].cursor() as cursor:
                query = f"INSERT INTO account_profile ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(query, values)
                
                # 새로 생성된 ID 가져오기
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_id = cursor.fetchone()[0]
                
                # 생성된 프로필 객체 반환
                return self.get(id=last_id)
        except Exception as e:
            print(f"DB 저장 오류: {e}")
            raise
    
    def save(self, profile):
        """
        기존 AccountProfile 객체를 저장
        """
        try:
            if profile.id:
                # 업데이트
                fields = []
                values = []
                
                if hasattr(profile, 'account_id') and profile.account_id is not None:
                    fields.append('account_id = %s')
                    values.append(profile.account_id)
                
                if hasattr(profile, 'nickname') and profile.nickname is not None:
                    fields.append('nickname = %s')
                    values.append(profile.nickname)
                
                if hasattr(profile, 'gender') and profile.gender is not None:
                    fields.append('gender = %s')
                    values.append(profile.gender)
                
                if hasattr(profile, 'birthyear') and profile.birthyear is not None:
                    fields.append('birthyear = %s')
                    values.append(profile.birthyear)
                
                if hasattr(profile, 'age_range') and profile.age_range is not None:
                    fields.append('age_range = %s')
                    values.append(profile.age_range)
                
                if fields:
                    values.append(profile.id)  # WHERE id = %s 조건에 사용
                    with connections[self.db_connection].cursor() as cursor:
                        query = f"UPDATE account_profile SET {', '.join(fields)} WHERE id = %s"
                        cursor.execute(query, values)
            else:
                # 새로 생성
                kwargs = {}
                if hasattr(profile, 'account_id') and profile.account_id is not None:
                    kwargs['account_id'] = profile.account_id
                elif hasattr(profile, '_account') and profile._account is not None:
                    kwargs['account'] = profile._account
                
                if hasattr(profile, 'nickname') and profile.nickname is not None:
                    kwargs['nickname'] = profile.nickname
                if hasattr(profile, 'gender') and profile.gender is not None:
                    kwargs['gender'] = profile.gender
                if hasattr(profile, 'birthyear') and profile.birthyear is not None:
                    kwargs['birthyear'] = profile.birthyear
                if hasattr(profile, 'age_range') and profile.age_range is not None:
                    kwargs['age_range'] = profile.age_range
                
                new_profile = self.create(**kwargs)
                profile.id = new_profile.id
            
            return profile
        except Exception as e:
            print(f"DB 저장 오류: {e}")
            raise


# 예외 클래스 추가 (Django ORM 호환성)
setattr(AccountProfile, 'DoesNotExist', type('DoesNotExist', (Exception,), {}))
setattr(AccountProfile, 'MultipleObjectsReturned', type('MultipleObjectsReturned', (Exception,), {}))
