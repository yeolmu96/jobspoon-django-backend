from abc import ABC, abstractmethod

class JobCrawlRepository(ABC):

    @abstractmethod
    def jobCrawl(self, source: str) -> list[dict]:
        pass
