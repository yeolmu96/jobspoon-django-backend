from django.db import models

from account.entity.role_type import RoleType


class AccountRoleType(models.Model):
    roleType = models.CharField(max_length=64, choices=RoleType.choices, default=RoleType.NORMAL)

    def __str__(self):
        return self.roleType

    class Meta:
        db_table = 'account_role_type'
        app_label = 'account'


