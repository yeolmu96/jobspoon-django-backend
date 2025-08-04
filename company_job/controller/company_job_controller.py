from rest_framework import viewsets, status
from django.http import JsonResponse

from company_job.service.company_job_service_impl import CompanyJobServiceImpl


class CompanyJobController(viewsets.ViewSet):
    __service = CompanyJobServiceImpl.getInstance()

    def requestCreateCompanyJobs(self, request):
        isSuccess = self.__service.createCompanyJobs()
        return JsonResponse({'success': isSuccess})

    def requestCompanyJobList(self, request):
        try:
            jobListDataFrame = self.__service.getCompanyJobs()
            print(f"[Controller] companyJobList: {jobListDataFrame}")

            return JsonResponse(jobListDataFrame.to_dict(orient='records'), safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
