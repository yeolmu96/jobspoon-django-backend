from orders.entity.order_item import OrderItems
from orders.repository.order_item_repository import OrderItemRepository

# 주문 항목 데이터 접근 구현체 (싱글톤)
class OrderItemRepositoryImpl(OrderItemRepository):
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

    def save(self, orderItem):
        orderItem.save()
        return orderItem

    def bulkCreate(self, orderItemList):
        for orderItem in orderItemList:
            print(f"bulkCreate() orderItem: {orderItem}")
            if not orderItem.orders:
                raise Exception(f"Order item with ID {orderItem.id} has no associated order.")
            print(
                f"Order ID: {orderItem.orders.id}, MembershipPlan ID: {orderItem.membership_plan.id}, Quantity: {orderItem.quantity}, Price: {orderItem.price}")

        OrderItems.objects.bulk_create(orderItemList)