from abc import ABC, abstractmethod


class ImageGalleryService(ABC):

    @abstractmethod
    def requestList(self, page, perPage):
        pass

    @abstractmethod
    def requestCreate(self, title, image_url):
        pass
