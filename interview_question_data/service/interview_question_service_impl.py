from interview_question_data.entity.interview_data import InterviewData
from interview_question_data.repository.interview_question_repository_impl import InterviewQuestionRepositoryImpl
from interview_question_data.service.interview_question_service import InterviewQuestionService
from interview.repository.interview_repository_impl import InterviewRepositoryImpl

import pandas as pd


# 질문 관련 서비스 구현체
class InterviewQuestionServiceImpl(InterviewQuestionService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repository = InterviewQuestionRepositoryImpl.getInstance()
            cls.__instance.interviewRepository = InterviewRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        return cls()

    def saveQuestions(self, interview_id: int, question_list: list) -> list:
        # 인터뷰 존재 여부 확인
        interview = self.interviewRepository.findById(interview_id)
        if not interview:
            raise Exception("해당 인터뷰가 존재하지 않습니다.")

        # 전체 질문 텍스트 수집 (중복 제거 용도)
        existing_questions = set(self.repository.findAllQuestionTexts())
        saved_questions = []

        for text in question_list:
            if text in existing_questions:
                continue  # 중복은 저장하지 않음
            q = InterviewData(interview=interview, question_text=text)
            saved = self.repository.save(q)
            saved_questions.append(saved)
            existing_questions.add(text)  # 메모리에도 추가하여 중복 방지

        return saved_questions

    def getQuestions(self, interview_id: int):
        # 특정 인터뷰의 질문 목록 조회
        return self.repository.findByInterviewId(interview_id)

    def import_questions_from_excel(self, file_path):
        #
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            InterviewQuestionRepositoryImpl.create_question(
                question=row.get('question', ''),
                category=row.get('category', ''),
                source=row.get('source', '')
            )

    def list_questions(self):
        return InterviewQuestionRepositoryImpl.get_all_questions()