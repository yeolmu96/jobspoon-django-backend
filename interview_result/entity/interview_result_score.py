from django.db import models
from interview_result.entity.interview_result import InterviewResult

class InterviewResultScore(models.Model):
    # 면접 결과 1건과 1:1로 연결
    interview_result = models.OneToOneField(
        InterviewResult,
        on_delete=models.CASCADE,      # 관련 면접 결과 삭제되면 이 점수도 삭제됨
        related_name='score'          # interview_result.score 로 접근 가능
    )

    # 6각형 점수 항목들
    productivity = models.FloatField(default=0.0)        # 생산성
    communication = models.FloatField(default=0.0)       # 의사소통
    technical_skills = models.FloatField(default=0.0)    # 개발 역량 (기존: development)
    documentation_skills = models.FloatField(default=0.0)# 문서 작성 (기존: documentation)
    flexibility = models.FloatField(default=0.0)         # 유연성
    problem_solving = models.FloatField(default=0.0)     # 문제해결능력 (기존: decision_making)

    class Meta:
        db_table = 'interview_result_score'              # 실제 DB 테이블 이름
        app_label = 'interview_result'                   # Django 앱 이름과 일치시켜야 함
