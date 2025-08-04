from abc import ABC, abstractmethod


class ImageGalleryRepository(ABC):

    @abstractmethod
    def list(self, page, perPage):
        pass

    @abstractmethod
    def save(self, title, image_url):
        pass
