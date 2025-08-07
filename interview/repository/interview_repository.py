from abc import ABC, abstractmethod
from typing import List, Optional


class InterviewRepository(ABC):

    @abstractmethod
    def save(self, interview) -> object:
        """인터뷰를 저장합니다."""
        pass

    @abstractmethod
    def saveQuestion(self, interview_id: int, question: str) -> int | None:
        pass

    @abstractmethod
    def findById(self, interviewId: int) -> Optional[object]:
        """인터뷰 ID로 인터뷰를 찾습니다."""
        pass

    @abstractmethod
    def findInterviewByAccount(self, account, page: int, pageSize: int) -> List[object]:
        """특정 계정에 해당하는 인터뷰 목록을 반환합니다. 페이지네이션 적용"""
        pass

    @abstractmethod
    def deleteById(self, interviewId: int) -> bool:
        """인터뷰를 ID로 삭제합니다."""
        pass