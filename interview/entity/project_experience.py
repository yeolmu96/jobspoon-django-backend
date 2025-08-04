from django.db.models import IntegerChoices


class ProjectExperience(IntegerChoices):
    NO_PROJECT = 1, "없음"
    HAS_PROJECT = 2, "있음"
