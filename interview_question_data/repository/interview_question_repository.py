from abc import ABC, abstractmethod
from typing import List
from interview_question_data.entity.interview_data import InterviewData

# 질문 저장소 인터페이스 정의
class InterviewQuestionRepository(ABC):

    # @abstractmethod
    # def save(self, question: InterviewQuestion) -> InterviewQuestion:
    #     # 질문 저장
    #     pass
    #
    # @abstractmethod
    # def findByInterviewId(self, interview_id: int) -> List[InterviewQuestion]:
    #     # 특정 인터뷰 ID로 질문 목록 조회
    #     pass
    #
    # @abstractmethod
    # def findAllQuestionTexts(self) -> list:
    #     # 전체 질문 텍스트만 리스트로 반환
    #     pass

    @abstractmethod
    def create_question(self, question, category=None, source=None):
        pass

    @abstractmethod
    def get_all_questions(self):
        pass

    @abstractmethod
    def find_by_category(self, category):
        pass
