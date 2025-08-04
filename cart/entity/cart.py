from django.db import models

from account.entity.account import Account


class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    accountId = models.BigIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart -> id: {self.cartId}, account: {self.account.id}"

    class Meta:
        db_table = 'cart'
        app_label = 'cart'