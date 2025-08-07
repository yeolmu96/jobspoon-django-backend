from django.db import models

# 구독 상품 정의 엔티티
class Membership(models.Model):
    PLAN_TYPE_CHOICES = [
        ('DAY', '1일권'),
        ('WEEK', '1주일권'),
        ('MONTH', '1개월권')
    ]

    name = models.CharField(max_length=100)  # 상품명
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 가격
    duration_days = models.PositiveIntegerField()  # 구독 유효 기간 (일 수)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)  # 플랜 종류 코드
    is_active = models.BooleanField(default=True)  # 현재 사용 가능 여부

    class Meta:
        db_table = 'membership'

    def __str__(self):
        # 예: '프리미엄 (1개월권)'
        return f"{self.name} ({self.get_plan_type_display()})"