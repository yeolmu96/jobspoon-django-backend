from django.db import models

class InterviewQuestion(models.Model):
    interview = models.ForeignKey("Interview", on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()  # 인터뷰 질문이 여기에 들어감
    created_at = models.DateTimeField(auto_now_add=True)  # 언제 생성됐는지

    class Meta:
        db_table = 'interview_question_data'
        app_label = 'interview'