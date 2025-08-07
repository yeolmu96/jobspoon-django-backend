from abc import ABC, abstractmethod


class PaymentsRepository(ABC):

    @abstractmethod
    def request(self, paymentRequestData):
        pass

    @abstractmethod
    def create(self, payments):
        pass
