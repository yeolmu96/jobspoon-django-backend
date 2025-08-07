from django.db import models

from account.entity.account import Account

class AdminProfile(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32, unique=True)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )

    class Meta:
        db_table = 'admin_profile'
        app_label = 'account_profile'
