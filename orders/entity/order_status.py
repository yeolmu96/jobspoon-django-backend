from django.db import models

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', '결제 대기'
    COMPLETED = 'COMPLETED', '구독 완료'
    SHIPPING = 'SHIPPING', '구독 중'
