from abc import ABC, abstractmethod

class ReportCrawlRepository(ABC):

    @abstractmethod
    def reportCrawl(self, source: str) -> list[dict]:
        pass
