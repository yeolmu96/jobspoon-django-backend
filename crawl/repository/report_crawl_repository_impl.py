# 📄 crawl/repository/company_crawl_repository_impl.py

from crawl.report.jobplanet_report import crawl_jobplanet_report
from crawl.report.jobkorea_report import crawl_jobkorea_report
from crawl.report.wanted_report import crawl_wanted_report


class CompanyCrawlRepositoryImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CompanyCrawlRepositoryImpl, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def reportCrawl(self, source: str) -> list[dict]:
        if source == "잡플래닛":
            return crawl_jobplanet_report()
        elif source == "잡코리아":
            return crawl_jobkorea_report()
        elif source == "원티드":
            return crawl_wanted_report()
        else:
            raise ValueError(f"Unknown source for company crawl: {source}")
