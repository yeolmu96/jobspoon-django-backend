from django.db import models

class CompanyJob(models.Model):
    source = models.CharField(max_length=30, null=True, blank=True)        # 예: '당근', '토스'
    company_name = models.CharField(max_length=100, null=True, blank=True) # 회사명
    job_title = models.CharField(max_length=200, null=True, blank=True)    # 채용 제목
    post_url = models.URLField(null=True, blank=True)                      # 채용공고 URL
    posted_at = models.DateTimeField(null=True, blank=True)                # 공고 게시일
    description = models.TextField(null=True, blank=True)                  # 공고 요약 or 본문

    def __str__(self):
        return f"[{self.source}] {self.company_name} - {self.job_title}"

    class Meta:
        db_table = 'company_job'
