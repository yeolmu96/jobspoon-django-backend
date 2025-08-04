from abc import ABC, abstractmethod
from typing import List
from company_report.entity.company_report import CompanyReport

class CompanyReportRepository(ABC):

    @abstractmethod
    def create(self, data: dict) -> CompanyReport:
        pass

    @abstractmethod
    def create_many(self, data_list: List[dict]) -> List[CompanyReport]:
        pass

    @abstractmethod
    def find_all(self) -> List[CompanyReport]:
        pass
