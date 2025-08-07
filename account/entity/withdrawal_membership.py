from django.db import models

class WithdrawalMembership(models.Model):
    id = models.AutoField(primary_key=True)
    accountId = models.CharField(max_length=50)   # 이 accountId는 redis에서 오는 정보를 담아애함.
    #reason = models.CharField(max_length=50)  # 이건 아직 구현 안함 (프론트에서 받은 reason을 DB에 넣는것)
    withdraw_at = models.DateTimeField(null=True)  # 탈퇴 시점
    withdraw_end = models.DateTimeField(null=True)   # 탈퇴 시점을 시작으로 3년


    class Meta:
        db_table = 'withdrawal_membership'
        app_label = 'account'


    def getId(self):
        return self.id

    def getAccountId(self):
        return self.accountId

