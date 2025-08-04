from django.db import models

class CompanyReport(models.Model):
    source = models.CharField(max_length=50)  # 예: 잡플래닛, 잡코리아
    company_name = models.CharField(max_length=100)
    rating = models.FloatField(null=True, blank=True)         # 회사 평점
    overview = models.TextField(null=True, blank=True)        # 한줄소개 / 기업 개요
    welfare = models.TextField(null=True, blank=True)         # 복지 정보
    salary_info = models.TextField(null=True, blank=True)     # 연봉 관련 설명
    culture = models.TextField(null=True, blank=True)         # 조직문화, 분위기
    review_summary = models.TextField(null=True, blank=True)  # 좋아요/아쉬운점 요약
    collected_at = models.DateTimeField(auto_now_add=True)    # 수집 시각

    def __str__(self):
        return f"{self.company_name} ({self.source})"


