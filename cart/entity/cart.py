from django.db import models

from account.entity.account import Account


class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    # accountId 필드만 사용하고 account ForeignKey 제거
    accountId = models.BigIntegerField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    
    # account 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def account(self):
        """accountId를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.accountId)
    
    @account.setter
    def account(self, account):
        """account 설정 시 accountId도 함께 설정"""
        if account is not None:
            self.accountId = account.id
        else:
            self.accountId = None

    def __str__(self):
        return f"Cart -> id: {self.cartId}, accountId: {self.accountId}"

    class Meta:
        db_table = 'cart'
        app_label = 'cart'