from abc import ABC, abstractmethod

class OrderItemRepository(ABC):

    # 주문 항목 단일 저장
    @abstractmethod
    def save(self, orderItem):
        pass

    # 주문 항목 일괄 저장
    @abstractmethod
    def bulkCreate(self, orderItemList):
        pass