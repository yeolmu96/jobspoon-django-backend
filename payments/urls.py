from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payments.controller.payments_controller import PaymentsController

router = DefaultRouter()
router.register(r"payments", PaymentsController, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('process',
         PaymentsController.as_view({ 'post': 'requestProcessPayments' }),
         name='결제 진행'),
]