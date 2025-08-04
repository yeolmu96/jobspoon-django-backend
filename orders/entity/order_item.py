from django.db import models

from membership_plan.entity.membership import Membership
from orders.entity.orders import Orders


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    orders = models.ForeignKey(Orders, related_name="items", on_delete=models.PROTECT)  # Order와 연결
    membership_plan = models.ForeignKey(Membership, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item: {self.quantity} x {self.price}"

    class Meta:
        db_table = 'orders_items'
        app_label = 'orders'