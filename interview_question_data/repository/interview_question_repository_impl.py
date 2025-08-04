from interview_question_data.entity.interview_data import InterviewData
from interview_question_data.repository.interview_question_repository import InterviewQuestionRepository

# 질문 저장소 구현체
class InterviewQuestionRepositoryImpl(InterviewQuestionRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        return cls()

    # def save(self, question: InterviewQuestion) -> InterviewQuestion:
    #     # 질문 저장 후 반환
    #     question.save()
    #     return question
    #
    # def findByInterviewId(self, interview_id: int):
    #     # 특정 인터뷰 ID에 해당하는 질문 목록 조회
    #     return InterviewQuestion.objects.filter(interview_id=interview_id).order_by("created_at")
    #
    # def findAllQuestionTexts(self) -> list:
    #     # DB 전체에서 질문 텍스트만 추출
    #     return InterviewQuestion.objects.values_list("question_text", flat=True)

    def create_question(self, question, category=None, source=None):
        return InterviewData.objects.create(
            question=question,
            category=category,
            source=source
        )

    def get_all_questions(self):
        return InterviewData.objects.all()

    def find_by_category(self, category):
        return InterviewData.objects.filter(category=category)

