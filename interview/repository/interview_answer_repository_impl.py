from interview.entity.interview_answer import InterviewAnswer


class InterviewAnswerRepositoryImpl:
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

    def save(self, interviewAnswer: InterviewAnswer) -> InterviewAnswer | None:
        try:
            interviewAnswer.save()  # Django ORM을 사용하여 DB에 저장
            return interviewAnswer
        except Exception as e:
            print(f"답변 저장 실패: {e}")
            return None