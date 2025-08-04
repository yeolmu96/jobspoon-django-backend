from django.db import models

from account.entity.account_role_type import AccountRoleType
from account.entity.account_login_type import AccountLoginType


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32)
    roleType = models.ForeignKey(AccountRoleType, on_delete=models.CASCADE)
    loginType = models.ForeignKey(AccountLoginType, on_delete=models.CASCADE)  # , related_name ="profile")


    def __str__(self):
        return f"Account(id={self.id}, email={self.email}, roleType={self.roleType}, loginType={self.loginType})"
    class Meta:
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
