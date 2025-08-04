
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company_report.controller.company_report_controller import CompanyReportController

router = DefaultRouter()
router.register(r'company_report', CompanyReportController, basename='company_report')

urlpatterns = [
    path('', include(router.urls)),
    path('request-create-company-reports',
         CompanyReportController.as_view({'get': 'requestCreateCompanyReports'}),
         name='회사 공고 크롤링'),
    path('request-company-report-list',
         CompanyReportController.as_view({'get': 'requestCompanyReportList'}),
         name='회사 공고 리스트'),
]
