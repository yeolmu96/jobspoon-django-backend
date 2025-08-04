from django.urls import path, include
from rest_framework.routers import DefaultRouter
from training_sample.controller.training_sample_controller import TrainingSampleController

router = DefaultRouter()
router.register(r"training_sample", TrainingSampleController, basename="training_sample")

urlpatterns = [
    path("", include(router.urls)),
]
