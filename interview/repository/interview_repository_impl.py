from django.core.paginator import Paginator, EmptyPage
from django.db import models
from interview.entity.interview import Interview
from interview.entity.interview_question import InterviewQuestion
from interview.repository.interview_repository import InterviewRepository


class InterviewRepositoryImpl(InterviewRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, interview) -> Interview:
        """인터뷰 저장"""
        interview.save()
        return interview

    def saveQuestion(self, interview_id: int, question: str) -> int | None:
        try:
            saved = InterviewQuestion.objects.create(
                interview_id=interview_id,
                content=question
            )
            return saved.id
        except Exception as e:
            print(f"❌ 질문 저장 실패: {e}")
            return None

    def findById(self, interviewId: int) -> Interview:
        """인터뷰 ID로 인터뷰 찾기"""
        try:
            return Interview.objects.get(id=interviewId)
        except Interview.DoesNotExist:
            return None

    def findInterviewByAccount(self, account, page: int, pageSize: int) -> models.QuerySet:
        """특정 계정에 해당하는 인터뷰 목록 조회 (페이지네이션 적용)"""
        interviews = Interview.objects.filter(account=account).order_by("-created_at")
        paginator = Paginator(interviews, pageSize)
        try:
            page = paginator.page(page)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page

    def deleteById(self, interviewId: int) -> bool:
        """인터뷰 ID로 인터뷰 삭제"""
        try:
            interview = Interview.objects.get(id=interviewId)
            interview.delete()
            return True
        except Interview.DoesNotExist:
            return False