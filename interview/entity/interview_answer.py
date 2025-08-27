from django.db import models
from account.entity.account import Account

class InterviewAnswer(models.Model):
    # Account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()
    interview = models.ForeignKey('interview.Interview', on_delete=models.CASCADE)
    question = models.ForeignKey('interview.InterviewQuestion', on_delete=models.CASCADE)
    answer_text = models.TextField()   # 여기에 면접 질문 들어감

    created_at = models.DateTimeField(auto_now_add=True)
    
    # account 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def account(self):
        """account_id를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.account_id)
    
    @account.setter
    def account(self, account):
        """account 설정 시 account_id도 함께 설정"""
        if account is not None:
            self.account_id = account.id
        else:
            self.account_id = None

    class Meta:
        db_table = 'interview_answer'
        app_label = 'interview'

    def __str__(self):
        return f"Answer for Interview {self.interview.id} - Question {self.question.id}"
