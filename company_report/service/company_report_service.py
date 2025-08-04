from abc import ABC, abstractmethod

class CompanyReportService(ABC):

    @abstractmethod
    def createCompanyReports(self):
        pass

    @abstractmethod
    def getCompanyReports(self):
        pass
