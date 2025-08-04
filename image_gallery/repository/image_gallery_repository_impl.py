from django.db import IntegrityError

from image_gallery.entity.image_gallery import ImageGallery
from image_gallery.repository.image_gallery_repository import ImageGalleryRepository


class ImageGalleryRepositoryImpl(ImageGalleryRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self, page, perPage):
        offset = (page - 1) * perPage
        imageGallery = ImageGallery.objects.all().order_by('-created_at')[offset:offset + perPage]
        totalItems = ImageGallery.objects.count()

        return imageGallery, totalItems

    def save(self, title, image_url):
        ImageGallery.objects.create(title=title, image_url=image_url)
