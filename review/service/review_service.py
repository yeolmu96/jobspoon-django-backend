from abc import ABC, abstractmethod


class ReviewService(ABC):

    @abstractmethod
    def requestList(self, page, perPage):
        pass

    @abstractmethod
    def requestUploadToS3(self, file, title):
        pass

    @abstractmethod
    def requestCreate(self, title, content, accountId):
        pass

    @abstractmethod
    def requestRead(self, id):
        pass

    @abstractmethod
    def requestDelete(self, boardId, accountId):
        pass
