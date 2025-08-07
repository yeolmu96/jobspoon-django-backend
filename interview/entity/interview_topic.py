from django.db.models import IntegerChoices

class InterviewTopic(IntegerChoices):
    BACKEND = 1, "BACKEND"
    FRONTEND = 2, "FRONTEND"
    EMBEDDED = 3, "EMBEDDED"
    AI = 4, "AI"
    DEVOPS = 5, "DEVOPS"
    WEBAPP = 6, "WEBAPP"