from rest_framework import viewsets, status
from rest_framework.response import Response
from company_report.service.company_report_service_impl import CompanyReportServiceImpl

class CompanyReportController(viewsets.ViewSet):
    CompanyReportService = CompanyReportServiceImpl.getInstance()

    # 기업 정보 수집 요청 (크롤링 → 저장)
    def requestCreateCompanyReports(self, request):
        self.CompanyReportService.createCompanyReports()
        return Response({"message": "기업 정보 수집 완료"}, status=status.HTTP_200_OK)

    # 저장된 기업 정보 전체 조회
    def requestCompanyReportList(self, request):
        reports = self.CompanyReportService.getCompanyReports()
        serialized = [
            {
                "company_name": r.company_name,
                "source": r.source,
                "rating": r.rating,
                "overview": r.overview,
                "welfare": r.welfare,
                "salary_info": r.salary_info,
                "culture": r.culture,
                "review_summary": r.review_summary,
                "collected_at": r.collected_at
            }
            for r in reports
        ]
        return Response(serialized, status=status.HTTP_200_OK)
