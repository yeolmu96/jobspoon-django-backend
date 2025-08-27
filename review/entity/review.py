from django.db import models

from account.entity.account import Account


class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # writer ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    writer_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    # writer 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def writer(self):
        """writer_id를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.writer_id)
    
    @writer.setter
    def writer(self, writer):
        """writer 설정 시 writer_id도 함께 설정"""
        if writer is not None:
            self.writer_id = writer.id
        else:
            self.writer_id = None

    class Meta:
        db_table = "review"
        app_label = "review"
