from abc import abstractmethod, ABC


class MarketingRepository(ABC):
    @abstractmethod
    def makeCount(self, email,product_id,purchase):
        pass