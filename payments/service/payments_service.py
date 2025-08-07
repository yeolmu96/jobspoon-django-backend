from abc import ABC, abstractmethod


class PaymentsService(ABC):

    @abstractmethod
    def process(self, accountId, paymentKey, orderId, amount, orderInfoId):
        pass
