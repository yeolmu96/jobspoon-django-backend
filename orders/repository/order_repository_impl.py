from orders.entity.orders import Orders
from orders.repository.order_repository import OrderRepository


class OrderRepositoryImpl(OrderRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def save(self, order):
        order.save()
        return order

    def findById(self, orderId):
        try:
            return Orders.objects.get(id=orderId)
        except Orders.DoesNotExist:
            return None