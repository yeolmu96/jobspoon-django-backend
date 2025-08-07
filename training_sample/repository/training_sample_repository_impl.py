from training_sample.entity.training_question import TrainingQuestion
from training_sample.entity.training_answer import TrainingAnswer
from training_sample.repository.training_sample_repository import TrainingSampleRepository

class TrainingSampleRepositoryImpl(TrainingSampleRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        return cls()

    def save_question(self, question: str, category: str):
        return TrainingQuestion.objects.create(question=question, category=category)

    def save_answer(self, question_text: str, answer: str):
        question = TrainingQuestion.objects.get(question=question_text)
        return TrainingAnswer.objects.create(question=question, answer=answer)

    def get_all_samples(self):
        return [
            {"question": ans.question.question, "answer": ans.answer}
            for ans in TrainingAnswer.objects.select_related("question").all()
        ]
