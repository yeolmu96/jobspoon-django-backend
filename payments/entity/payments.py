from django.db import models

from account.entity.account import Account
from orders.entity.orders import Orders


class Payments(models.Model):
    # account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()  # 결제 소유자 ID
    payment_key = models.CharField(max_length=255)  # 결제 키
    order_id = models.CharField(max_length=255)  # 주문 ID
    orders_info = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')  # 외래키로 Orders 모델 연결
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 결제 금액
    provider = models.CharField(max_length=100)  # 결제 제공자
    method = models.CharField(max_length=100)  # 결제 방법
    paid_at = models.DateTimeField()  # 결제 승인 시간
    receipt_url = models.URLField()  # 영수증 URL

    created_at = models.DateTimeField(auto_now_add=True)  # 결제 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 결제 정보 수정 시간

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
        return f"Payment {self.payment_key} for Order {self.order_id} (Account ID: {self.account_id})"

    class Meta:
        db_table = 'payments'
        app_label = 'payments'
