from django.db import models
from account.entity.account import Account
from interview.entity.academic_background import AcademicBackground
from interview.entity.company_name import CompanyName
from interview.entity.experience_level import ExperienceLevel
from interview.entity.interview_status import InterviewStatus
from interview.entity.interview_topic import InterviewTopic
from interview.entity.project_experience import ProjectExperience
from interview.entity.tech_stack import TechStack

class Interview(models.Model):
    id = models.AutoField(primary_key=True)
    # account ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    account_id = models.IntegerField()
    
    # account 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def account(self):
        """account_id를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.account_id)
    
    @account.setter
    def account(self, account):
        """account 설정 시 account_id도 함께 설정"""
        if account is not None:
            self.account_id = account.id
        else:
            self.account_id = None


    topic = models.CharField(
        max_length=50,
        choices=InterviewTopic.choices
    )
    experience_level = models.IntegerField(
        choices=ExperienceLevel.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=InterviewStatus.choices,
        default=InterviewStatus.IN_PROGRESS,
    )
    project_experience  = models.IntegerField(
        choices=ProjectExperience.choices,
    )
    academic_background = models.IntegerField(
        choices=AcademicBackground.choices,
        default=AcademicBackground.NON_MAJOR  # 기본값: 비전공자
    )
    tech_stack = models.JSONField(blank=False, null=False)
    company_name = models.CharField(
        max_length=20,
        choices=CompanyName.choices,
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interview'
        app_label = 'interview'

    def __str__(self):
        return (
            f"Interview(id={self.id}, account={self.account}, topic={self.topic}, "
            f"experience_level={self.experience_level}, status={self.status}, "
            f"project_experience={self.project_experience}, "
            f"academic_background={self.academic_background}, "
            f"tech_stack={self.tech_stack})"
            f"company_name={self.company_name}"
        )

    def getId(self):
        return self.id

    def getAccount(self):
        return self.account

    def getTopic(self):
        return self.topic

    def getExperienceLevel(self):
        return ExperienceLevel(self.experience_level)

    def getStatus(self):
        return self.status

    def getProjectExperience(self):
        return ProjectExperience(self.project_experience)

    def getAcademicBackground(self):
        return AcademicBackground(self.academic_background)

    def getTechStack(self):
        raw = self.tech_stack

        if isinstance(raw, list):
            return [TechStack(sid) for sid in raw if isinstance(sid, int)]
        elif isinstance(raw, int):
            try:
                return [TechStack(raw)]
            except ValueError:
                print(f"[경고] 유효하지 않은 단일 tech_stack ID: {raw}")
                return []
        else:
            print(f"[경고] tech_stack 타입 오류: {raw}")
            return []

    def getCompanyName(self):
        return CompanyName(self.company_name)