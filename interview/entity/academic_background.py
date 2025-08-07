from django.db.models import IntegerChoices


class AcademicBackground(IntegerChoices):
    NON_MAJOR = 1, "비전공자"
    MAJOR = 2, "전공자"
