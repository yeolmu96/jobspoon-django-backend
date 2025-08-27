from django.db import models

from account.entity.account import Account

class AdminProfile(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32, unique=True)
    # OneToOneField를 account_id로 변경
    account_id = models.IntegerField(unique=True)  # 회원과 1:1 관계를 유지하기 위해 unique=True 설정

    # account 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def account(self):
        """
        account_id를 통해 Account 객체를 필요할 때만 로드
        """
        if not hasattr(self, '_account') or self._account is None:
            self._account = Account.objects().get(id=self.account_id)
        return self._account
    
    @account.setter
    def account(self, account):
        """
        account 설정 시 account_id도 함께 설정
        """
        self._account = account
        if account is not None:
            self.account_id = account.id
        else:
            self.account_id = None

    class Meta:
        db_table = 'admin_profile'
        app_label = 'account_profile'
