from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.controller.order_controller import OrderController

router = DefaultRouter()
router.register(r"orders", OrderController, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('create',
         OrderController.as_view({ 'post': 'requestCreateOrder' }),
         name='주문 생성'),
]