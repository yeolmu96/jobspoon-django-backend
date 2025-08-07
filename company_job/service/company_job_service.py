from abc import ABC, abstractmethod

class CompanyJobService(ABC):

    @abstractmethod
    def createCompanyJobs(self):
        pass

    @abstractmethod
    def getCompanyJobs(self):
        pass
