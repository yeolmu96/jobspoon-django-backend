from django.db import models

from account.entity.login_type import LoginType


class AccountLoginType(models.Model):
    loginType = models.CharField(max_length=10, choices=LoginType.choices, default=None, null=True)

    def __str__(self):
        return self.loginType

    class Meta:
        db_table = 'account_login_type'
        app_label = 'account_profile'