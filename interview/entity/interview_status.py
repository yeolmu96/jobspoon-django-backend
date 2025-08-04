from django.db import models

class InterviewStatus(models.TextChoices):
    IN_PROGRESS = 'IN_PROGRESS', '진행 중'
    COMPLETED = 'COMPLETED', '완료'

    @classmethod
    def is_valid(cls, value):
        return value in cls.values

    @classmethod
    def values(cls):
        return [choice[0] for choice in cls.choices]