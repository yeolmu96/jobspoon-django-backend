from abc import ABC, abstractmethod

class CompanyJobRepository(ABC):

    @abstractmethod
    def createMany(self, jobDataList):
        pass

    @abstractmethod
    def findAll(self):
        pass
