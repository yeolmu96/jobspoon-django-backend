from company_report.entity.company_report import CompanyReport
from company_report.repository.company_report_repository import CompanyReportRepository

class CompanyReportRepositoryImpl(CompanyReportRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CompanyReportRepositoryImpl, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create(self, data: dict) -> CompanyReport:
        return CompanyReport.objects.create(**data)

    def create_many(self, data_list: list[dict]) -> list[CompanyReport]:
        return [self.create(data) for data in data_list]

    def find_all(self) -> list[CompanyReport]:
        return list(CompanyReport.objects.all())
