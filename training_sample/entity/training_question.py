from django.db import models

class TrainingQuestion(models.Model):
    question = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, default='엑셀 업로드')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'training_question'

    def __str__(self):
        return self.question[:50]
