from django.db import models

from account.entity.account import Account
from orders.entity.order_status import OrderStatus


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    # account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()
    # account 객체는 프로퍼티를 통해 필요할 때만 로드
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)  # 주문 상태
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간

    # account 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def account(self):
        """account_id를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.account_id)
    
    @account.setter
    def account(self, account):
        """account 설정 시 account_id도 함께 설정"""
        if account is not None:
            self.account_id = account.id
        else:
            self.account_id = None

    def __str__(self):
        return f"Order {self.id} by account_id {self.account_id}"

    class Meta:
        db_table = 'orders'
        app_label = 'orders'

    def getId(self):
        return self.id
