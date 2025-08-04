from crawl.job.google_search_job import crawl_google_search_jobs
from crawl.job.jobkorea_job import crawl_jobkorea_jobs
from crawl.job.jobplanet_company import crawl_jobplanet_company_info
from crawl.repository.job_crawl_repository import JobCrawlRepository
from crawl.job.daangn_job import crawl_daangn_jobs
from crawl.job.toss_job import crawl_toss_jobs
from crawl.job.wanted_job import crawl_wanted_jobs
from crawl.job.saramin_job import crawl_saramin_jobs

class JobCrawlRepositoryImpl(JobCrawlRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(JobCrawlRepositoryImpl, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def jobCrawl(self, source: str) -> list[dict]:
        if source == "당근":
            return crawl_daangn_jobs()
        elif source == "토스":
            return crawl_toss_jobs()
        elif source == "원티드":
            return crawl_wanted_jobs()
        elif source == "사람인":
            return crawl_saramin_jobs()
        elif source == "잡코리아":
            return crawl_jobkorea_jobs()
        elif source == "잡플래닛":
            return crawl_jobplanet_company_info()
        elif source == "구글-원티드":
            return crawl_google_search_jobs("당근마켓", "wanted.co.kr")
        else:
            raise ValueError(f"Unknown source: {source}")
