from django.db import models

class InterviewAnswer(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    interview = models.ForeignKey('interview.Interview', on_delete=models.CASCADE)
    question = models.ForeignKey('interview.InterviewQuestion', on_delete=models.CASCADE)
    answer_text = models.TextField()   # 여기에 면접 질문 들어감

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interview_answer'
        app_label = 'interview'

    def __str__(self):
        return f"Answer for Interview {self.interview.id} - Question {self.question.id}"
