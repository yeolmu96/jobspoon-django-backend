from django.db import models
from training_sample.entity.training_question import TrainingQuestion

class TrainingAnswer(models.Model):
    question = models.ForeignKey(TrainingQuestion, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()
    evaluator = models.CharField(max_length=50, default="human")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'training_answer'

    def __str__(self):
        return self.answer[:50]
