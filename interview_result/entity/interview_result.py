from django.db import models

from account.entity.account import Account


class InterviewResult(models.Model):
    id = models.AutoField(primary_key=True)
    # account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()
    interview_id = models.IntegerField()  # ✅ 새로 추가된 필드

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
        return f"InterviewResult -> id: {self.id}, account_id: {self.account_id}"


    class Meta:
        db_table = 'interview_result'
        app_label = 'interview_result'