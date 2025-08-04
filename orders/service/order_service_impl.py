from django.db import transaction

from orders.entity.orders import Orders
from orders.entity.order_status import OrderStatus
from orders.entity.order_item import OrderItems
from orders.repository.order_item_repository_impl import OrderItemRepositoryImpl
from account.repository.account_repository_impl import AccountRepositoryImpl
from cart.repository.cart_repository_impl import CartRepositoryImpl
from membership_plan.repository.membership_repository_impl import MembershipRepositoryImpl
from membership_plan.service.membership_service_impl import MembershipServiceImpl


from orders.repository.order_repository_impl import OrderRepositoryImpl
from orders.service.order_service import OrderService


class OrderServiceImpl(OrderService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cartRepository = CartRepositoryImpl.getInstance()
            cls.__instance.__orderRepository = OrderRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__orderItemRepository = OrderItemRepositoryImpl.getInstance()
            cls.__instance.__membershipRepository = MembershipRepositoryImpl.getInstance()
            cls.__instance.__membershipService = MembershipServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @transaction.atomic
    def createOrder(self, accountId, items, total):
        account = self.__accountRepository.findById(accountId)

        if not account:
            raise Exception(f"Account id {accountId} 존재하지 않음.")

        # 2. 총 금액 검증
        if not isinstance(total, (int, float)) or total <= 0:
            raise Exception("유효하지 않은 총 금액입니다.")

        # 3. 주문 항목 검증
        if not items or not isinstance(items, list):
            raise Exception("유효하지 않은 주문 항목입니다.")

        order = Orders(
            account=account,
            total_amount=total,
            status=OrderStatus.PENDING,
        )
        order = self.__orderRepository.save(order)
        print(f"order 생성: {order}")

        orderItemList = []
        for item in items:
            membership = self.__membershipRepository.findById(item["id"])
            if not membership:
                raise Exception(f"Membership ID {item['id']} 존재하지 않음.")

            # 멤버쉽 구독생성
            self.__membershipService.createMembership(accountId, membership.id)

            orderItem = OrderItems(
                orders=order,  # order가 올바르게 연결되었는지 확인
                membership_plan=membership,
                quantity=1,
                price=membership.price
            )
            orderItemList.append(orderItem)

        print(f"orderItemList: {orderItemList}")

        if orderItemList:
            self.__orderItemRepository.bulkCreate(orderItemList)

        order.status = OrderStatus.COMPLETED
        self.__orderRepository.save(order)

        return order.getId()