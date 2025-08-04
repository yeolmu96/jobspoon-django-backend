from django.db import models


# 면접 질문 도메인 모델 정의
class InterviewData(models.Model):
    #id = models.AutoField(primary_key=True)  # 고유 ID
    category = models.CharField(max_length=100, blank=True, null=True)  # 직무 종류
    companyName = models.CharField(max_length=100, blank=True, null=True)   # 회사 이름
    question = models.TextField()  # 질문 내용
    source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'interview_question_data_per_job_category'
        #app_label = 'interview'

    def __str__(self):
        return self.question[:50]