from django.db import models
from django.utils import timezone
from account.entity.account import Account
from company_report.entity.company_report import CompanyReport


class Marketing(models.Model):
    id = models.AutoField(primary_key=True)
    # account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()
    product = models.ForeignKey(CompanyReport, on_delete=models.CASCADE, related_name='marketing')
    click_count = models.PositiveSmallIntegerField(default=1)
    purchase = models.BooleanField(default=False)
    last_click_date = models.DateTimeField(default=timezone.now)

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
        return f"Marketing -> id: {self.id}, account_id: {self.account_id}, product: {self.product}"

    class Meta:
        db_table = 'marketing'
        app_label = 'marketing'
