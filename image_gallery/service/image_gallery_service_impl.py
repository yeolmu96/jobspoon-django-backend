from image_gallery.repository.image_gallery_repository_impl import ImageGalleryRepositoryImpl
from image_gallery.service.image_gallery_service import ImageGalleryService


class ImageGalleryServiceImpl(ImageGalleryService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__imageGalleryRepository = ImageGalleryRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestList(self, page, perPage):
        paginatedImageGalleryList, totalItems = self.__imageGalleryRepository.list(page, perPage)

        totalPages = (totalItems + perPage - 1) // perPage

        paginatedFilteringImageGalleryList = [
            {
                "id": imageGallery.id,
                "title": imageGallery.title,
                "imageUrl": imageGallery.image_url
            }
            for imageGallery in paginatedImageGalleryList
        ]

        return paginatedFilteringImageGalleryList, totalItems, totalPages

    def requestCreate(self, title, image_url):
        self.__imageGalleryRepository.save(title, image_url)

