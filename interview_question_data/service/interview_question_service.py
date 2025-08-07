from abc import ABC, abstractmethod
from interview_question_data.entity.interview_data import InterviewData


# 질문 관련 비즈니스 로직 인터페이스
class InterviewQuestionService(ABC):

    @abstractmethod
    def saveQuestions(self, interview_id: int, question_list: list) -> list:
        # 질문 리스트 저장 (중복 방지 포함)
        pass

    @abstractmethod
    def getQuestions(self, interview_id: int) -> list:
        # 특정 인터뷰의 질문 목록 조회
        pass

    @abstractmethod
    def import_questions_from_excel(self, file_path):
        pass

    @abstractmethod
    def list_questions(self):
        pass
