from abc import ABC, abstractmethod


class OrderService(ABC):

    @abstractmethod
    def createOrder(self, accountId, items, total):
        pass