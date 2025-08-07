from django.db import models

from account.entity.account import Account


class AccountProfile(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=32, unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthyear = models.CharField(max_length=4, blank=True, null=True)
    age_range = models.CharField(max_length=10, blank=True, null=True)
    # gender = models.CharField(max_length=32, default="Unknown") # 성별 추가
    # birthyear = models.IntegerField(default="Unknown") # 생년월일 추가
    # age_range = models.CharField(max_length=32)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    class Meta:
        db_table = 'account_profile'
        app_label = 'account_profile'
