from abc import ABC, abstractmethod


class OrderRepository(ABC):

    # 주문 저장
    @abstractmethod
    def save(self, order):
        pass

    # 주문 ID로 조회
    @abstractmethod
    def findById(self, orderId):
        pass
