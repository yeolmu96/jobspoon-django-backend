
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company_job.controller.company_job_controller import CompanyJobController

router = DefaultRouter()
router.register(r'company_job', CompanyJobController, basename='company_job')

urlpatterns = [
    path('', include(router.urls)),
    path('request-create-company-jobs',
         CompanyJobController.as_view({'get': 'requestCreateCompanyJobs'}),
         name='채용 정보 크롤링'),
    path('request-company-job-list',
         CompanyJobController.as_view({'get': 'requestCompanyJobList'}),
         name='채용 정보 리스트'),
]
