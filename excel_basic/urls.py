from django.urls import path, include
from rest_framework.routers import DefaultRouter

from excel_basic.controller.excel_basic_controller import ExcelBasicController

router = DefaultRouter()
router.register(r"excel-basic", ExcelBasicController, basename='excel-basic')

urlpatterns = [
    path('', include(router.urls)),
    path('request-create-excel2db',
         ExcelBasicController.as_view({ 'get': 'requestCreateExcelInfo' }),
         name='excel 정보 데이터 생성'),
    path('request-create-db2excel',
         ExcelBasicController.as_view({ 'get': 'requestDatabaseToExcel' }),
         name='DB 데이터를 excel로 생성'),
]