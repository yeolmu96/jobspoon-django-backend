from company_report.service.company_report_service import CompanyReportService
from company_report.repository.company_report_repository_impl import CompanyReportRepositoryImpl
from crawl.repository.report_crawl_repository_impl import CompanyCrawlRepositoryImpl

class CompanyReportServiceImpl(CompanyReportService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CompanyReportServiceImpl, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.repository = CompanyReportRepositoryImpl()
        self.crawler = CompanyCrawlRepositoryImpl()

    def createCompanyReports(self):
        sources = ["잡플래닛", "잡코리아", "원티드"]

        for source in sources:
            try:
                crawled_data = self.crawler.reportCrawl(source)
                print(f"[Service] {source} 수집 성공: {len(crawled_data)}건")

                cleaned_data = self.__clean_data(crawled_data)
                self.repository.create_many(cleaned_data)

            except Exception as e:
                print(f"[Service] Error for {source}: {e}")

    def getCompanyReports(self):
        return self.repository.find_all()

    def __clean_data(self, data_list: list[dict]) -> list[dict]:
        for d in data_list:
            if "overview" in d and isinstance(d["overview"], str):
                d["overview"] = d["overview"].strip()
            if "rating" in d:
                try:
                    d["rating"] = float(d["rating"])
                except:
                    d["rating"] = None
        return data_list
