from abc import ABC, abstractmethod

from review.entity.review import Review


class ReviewRepository(ABC):

    @abstractmethod
    def list(self, page, perPage):
        pass

    @abstractmethod
    def uploadToS3(self, fileContent: str, filename: str):
        pass

    @abstractmethod
    def save(self, review: Review) -> Review:
        pass

    @abstractmethod
    def findById(self, boardId):
        pass

    @abstractmethod
    def deleteFromS3(self, filePath: str):
        pass

    @abstractmethod
    def deleteById(self, boardId):
        pass
