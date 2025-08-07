from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image_gallery.controller.image_gallery_controller import ImageGalleryController

router = DefaultRouter()
router.register(r"image-gallery", ImageGalleryController, basename='board')

urlpatterns = [
    path('', include(router.urls)),
    path('list',
         ImageGalleryController.as_view({ 'get': 'requestImageGalleryList' }),
         name='이미지 갤러리 항목 요청'),
    path('create',
         ImageGalleryController.as_view({ 'post': 'requestRegisterImage' }),
         name='이미지 등록 요청'),
    # path('read/<int:pk>',
    #      BoardController.as_view({ 'get': 'requestBoardRead' }),
    #      name='게시물 읽기 요청'),
    # path('modify/<int:pk>',
    #      BoardController.as_view({ 'put': 'requestBoardModify' }),
    #      name='게시물 수정 요청'),
    # path('delete/<int:pk>',
    #      BoardController.as_view({'delete': 'requestBoardDelete'}), 
    #      name='게시물 삭제 요청'),
]