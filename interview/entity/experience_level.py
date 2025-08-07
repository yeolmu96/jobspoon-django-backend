from django.db.models import IntegerChoices


class ExperienceLevel(IntegerChoices):
    ENTRY = 1, '신입'
    UNDER_3 = 2, '3년 이하'
    UNDER_5 = 3, '5년 이하'
    UNDER_10 = 4, '10년 이하'
    OVER_10 = 5, '10년 이상'
