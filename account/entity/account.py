# Non-ORM 버전의 Account 클래스
# Django Model을 상속받지 않고 일반 클래스로 구현

from django.db import connections
from account.entity.account_role_type import AccountRoleType
from account.entity.account_login_type import AccountLoginType


class Account:
    """
    Django Model을 상속받지 않고 일반 클래스로 구현한 Account 클래스
    기존 코드와의 호환성을 위해 동일한 메서드와 속성 유지
    """
    db_table = 'account'  # 테이블 이름 지정
    
    def __init__(self, id=None, email=None, roleType=None, loginType=None):
        self.id = id
        self.email = email
        self.roleType = roleType
        self.loginType = loginType
    
    def __str__(self):
        return f"Account(id={self.id}, email={self.email}, roleType={self.roleType}, loginType={self.loginType})"
    
    class Meta:
        # Django ORM과의 호환성을 위해 Meta 클래스 유지
        db_table = 'account'
        app_label = 'account'
    
    def getId(self):
        return self.id
    
    def getEmail(self):
        return self.email
    
    def getRoleType(self):
        return self.roleType
    
    def getLoginType(self):
        return self.loginType
    
    @staticmethod
    def objects():
        """
        Django ORM의 objects 매니저와 유사한 기능을 제공하는 메서드
        Account.objects().all(), Account.objects().filter() 등의 호출을 지원
        """
        return AccountManager()


class AccountManager:
    """
    Django ORM의 Manager와 유사한 기능을 제공하는 클래스
    """
    def __init__(self):
        self.db_connection = 'default'  # settings.py에 정의된 DB 연결 사용
    
    def all(self):
        """
        모든 Account 객체를 반환
        """
        try:
            accounts = []
            with connections[self.db_connection].cursor() as cursor:
                # account 테이블과 account_profile 테이블 조인
                cursor.execute("""
                    SELECT a.id, ap.email, a.role_type_id, a.login_type_id 
                    FROM account a 
                    LEFT JOIN account_profile ap ON a.id = ap.account_id
                """)
                rows = cursor.fetchall()
                for row in rows:
                    account = Account(
                        id=row[0],
                        email=row[1],  # account_profile의 email
                        roleType=self._get_role_type(row[2]),
                        loginType=self._get_login_type(row[3])
                    )
                    accounts.append(account)
            return accounts
        except Exception as e:
            print(f"DB 조회 오류: {e}")
            return []
    
    def get(self, **kwargs):
        """
        조건에 맞는 단일 Account 객체를 반환
        """
        try:
            conditions = []
            params = []
            join_needed = False
            table_prefix = 'a.'
            
            for key, value in kwargs.items():
                if key == 'id':
                    conditions.append(f'{table_prefix}id = %s')
                    params.append(value)
                elif key == 'email':
                    join_needed = True
                    conditions.append('ap.email = %s')
                    params.append(value)
                # 필요에 따라 더 많은 조건 추가 가능
            
            if not conditions:
                raise ValueError("검색 조건이 지정되지 않았습니다.")
            
            with connections[self.db_connection].cursor() as cursor:
                # 실제 DB 테이블 구조에 맞게 쿼리 수정
                query = f"""
                    SELECT a.id, ap.email, a.role_type_id, a.login_type_id 
                    FROM account a 
                    LEFT JOIN account_profile ap ON a.id = ap.account_id
                    WHERE {' AND '.join(conditions)}
                """
                
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    return Account(
                        id=row[0],
                        email=row[1],  # account_profile의 email
                        roleType=self._get_role_type(row[2]),
                        loginType=self._get_login_type(row[3])
                    )
            raise Account.DoesNotExist(f"조건에 맞는 Account가 없습니다: {kwargs}")
        except Exception as e:
            if not isinstance(e, Account.DoesNotExist):
                print(f"DB 조회 오류: {e}")
            raise
    
    def filter(self, **kwargs):
        """
        조건에 맞는 여러 Account 객체를 반환
        """
        try:
            accounts = []
            conditions = []
            params = []
            join_needed = False
            table_prefix = 'a.'
            
            for key, value in kwargs.items():
                if key == 'id':
                    conditions.append(f'{table_prefix}id = %s')
                    params.append(value)
                elif key == 'email':
                    join_needed = True
                    conditions.append('ap.email = %s')
                    params.append(value)
                # 필요에 따라 더 많은 조건 추가 가능
            
            # 기본 쿼리 - account와 account_profile 테이블 조인
            query = """
                SELECT a.id, ap.email, a.role_type_id, a.login_type_id 
                FROM account a 
                LEFT JOIN account_profile ap ON a.id = ap.account_id
            """
            
            if conditions:
                query += f" WHERE {' AND '.join(conditions)}"
            
            with connections[self.db_connection].cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                for row in rows:
                    account = Account(
                        id=row[0],
                        email=row[1],  # account_profile의 email
                        roleType=self._get_role_type(row[2]),
                        loginType=self._get_login_type(row[3])
                    )
                    accounts.append(account)
            return accounts
        except Exception as e:
            print(f"DB 조회 오류: {e}")
            return []
    
    def create(self, **kwargs):
        """
        새로운 Account 객체를 생성하고 저장
        """
        try:
            # account 테이블에 들어갈 필드와 값
            account_fields = []
            account_values = []
            account_placeholders = []
            
            # account_profile 테이블에 들어갈 필드와 값
            profile_fields = []
            profile_values = []
            profile_placeholders = []
            
            email = None
            
            for key, value in kwargs.items():
                if key == 'email':
                    email = value
                    # email은 account_profile 테이블에 저장
                    profile_fields.append('email')
                    profile_values.append(value)
                    profile_placeholders.append('%s')
                elif key == 'roleType':
                    account_fields.append('role_type_id')
                    account_values.append(value.id)
                    account_placeholders.append('%s')
                elif key == 'loginType':
                    account_fields.append('login_type_id')
                    account_values.append(value.id)
                    account_placeholders.append('%s')
            
            with connections[self.db_connection].cursor() as cursor:
                # 1. account 테이블에 레코드 생성
                if account_fields:
                    account_query = f"INSERT INTO account ({', '.join(account_fields)}) VALUES ({', '.join(account_placeholders)})"
                    cursor.execute(account_query, account_values)
                    
                    # 새로 생성된 account ID 가져오기
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    account_id = cursor.fetchone()[0]
                    
                    # 2. 만약 email이 있다면 account_profile 테이블에도 레코드 생성
                    if email:
                        profile_fields.append('account_id')
                        profile_values.append(account_id)
                        profile_placeholders.append('%s')
                        
                        # nickname이 필수라면 기본값 설정
                        if 'nickname' not in profile_fields:
                            profile_fields.append('nickname')
                            profile_values.append(f"user_{account_id}")
                            profile_placeholders.append('%s')
                            
                        profile_query = f"INSERT INTO account_profile ({', '.join(profile_fields)}) VALUES ({', '.join(profile_placeholders)})"
                        cursor.execute(profile_query, profile_values)
                    
                    # 생성된 계정 객체 반환
                    return self.get(id=account_id)
                else:
                    raise ValueError("계정 생성에 필요한 필드가 없습니다.")
        except Exception as e:
            print(f"DB 저장 오류: {e}")
            raise
    
    def save(self, account):
        """
        기존 Account 객체를 저장
        """
        try:
            if account.id:
                # 업데이트
                # account 테이블 업데이트를 위한 필드와 값
                account_fields = []
                account_values = []
                
                # account_profile 테이블 업데이트를 위한 필드와 값
                profile_fields = []
                profile_values = []
                
                # account 테이블 업데이트
                if hasattr(account, 'roleType') and account.roleType is not None:
                    account_fields.append('role_type_id = %s')
                    account_values.append(account.roleType.id)
                
                if hasattr(account, 'loginType') and account.loginType is not None:
                    account_fields.append('login_type_id = %s')
                    account_values.append(account.loginType.id)
                
                # account_profile 테이블 업데이트
                if hasattr(account, 'email') and account.email is not None:
                    profile_fields.append('email = %s')
                    profile_values.append(account.email)
                
                with connections[self.db_connection].cursor() as cursor:
                    # account 테이블 업데이트
                    if account_fields:
                        account_values.append(account.id)  # WHERE id = %s 조건에 사용
                        account_query = f"UPDATE account SET {', '.join(account_fields)} WHERE id = %s"
                        cursor.execute(account_query, account_values)
                    
                    # account_profile 테이블 업데이트
                    if profile_fields:
                        # account_profile 테이블에서 account_id로 해당 프로필 찾기
                        cursor.execute("SELECT id FROM account_profile WHERE account_id = %s", [account.id])
                        profile_row = cursor.fetchone()
                        
                        if profile_row:  # 프로필이 존재하면 업데이트
                            profile_values.append(profile_row[0])  # WHERE id = %s 조건에 사용
                            profile_query = f"UPDATE account_profile SET {', '.join(profile_fields)} WHERE id = %s"
                            cursor.execute(profile_query, profile_values)
                        else:  # 프로필이 없으면 생성
                            # 프로필 생성에 필요한 필드와 값 추가
                            insert_fields = ['account_id']
                            insert_values = [account.id]
                            insert_placeholders = ['%s']
                            
                            if hasattr(account, 'email') and account.email is not None:
                                insert_fields.append('email')
                                insert_values.append(account.email)
                                insert_placeholders.append('%s')
                            
                            # nickname이 필수라면 기본값 설정
                            insert_fields.append('nickname')
                            insert_values.append(f"user_{account.id}")
                            insert_placeholders.append('%s')
                            
                            insert_query = f"INSERT INTO account_profile ({', '.join(insert_fields)}) VALUES ({', '.join(insert_placeholders)})"
                            cursor.execute(insert_query, insert_values)
            else:
                # 새로 생성
                kwargs = {}
                if hasattr(account, 'email') and account.email is not None:
                    kwargs['email'] = account.email
                if hasattr(account, 'roleType') and account.roleType is not None:
                    kwargs['roleType'] = account.roleType
                if hasattr(account, 'loginType') and account.loginType is not None:
                    kwargs['loginType'] = account.loginType
                
                new_account = self.create(**kwargs)
                account.id = new_account.id
            
            return account
        except Exception as e:
            print(f"DB 저장 오류: {e}")
            raise
    
    def _get_role_type(self, role_type_id):
        """
        role_type_id로 AccountRoleType 객체 가져오기
        """
        try:
            with connections[self.db_connection].cursor() as cursor:
                cursor.execute("SELECT id, role_name FROM account_role_type WHERE id = %s", [role_type_id])
                row = cursor.fetchone()
                if row:
                    role_type = AccountRoleType()
                    role_type.id = row[0]
                    role_type.role_name = row[1]
                    return role_type
            return None
        except Exception as e:
            print(f"RoleType 조회 오류: {e}")
            return None
    
    def _get_login_type(self, login_type_id):
        """
        login_type_id로 AccountLoginType 객체 가져오기
        """
        try:
            with connections[self.db_connection].cursor() as cursor:
                cursor.execute("SELECT id, login_name FROM account_login_type WHERE id = %s", [login_type_id])
                row = cursor.fetchone()
                if row:
                    login_type = AccountLoginType()
                    login_type.id = row[0]
                    login_type.login_name = row[1]
                    return login_type
            return None
        except Exception as e:
            print(f"LoginType 조회 오류: {e}")
            return None


# 예외 클래스 추가 (Django ORM 호환성)
setattr(Account, 'DoesNotExist', type('DoesNotExist', (Exception,), {}))
setattr(Account, 'MultipleObjectsReturned', type('MultipleObjectsReturned', (Exception,), {}))
