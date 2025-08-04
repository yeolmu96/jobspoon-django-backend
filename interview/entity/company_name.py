# interview/entity/company_name.py

from django.db.models import TextChoices

class CompanyName(TextChoices):
    danggeun = "danggeun", "당근"
    toss = "toss", '토스'
    sk_encore = "sk_encore", "SK엔코아"
    kt_mobile= "kt_mobile", "KT모바일"