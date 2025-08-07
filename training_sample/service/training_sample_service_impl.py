import pandas as pd
from training_sample.repository.training_sample_repository_impl import TrainingSampleRepositoryImpl
from training_sample.service.training_sample_service import TrainingSampleService

class TrainingSampleServiceImpl(TrainingSampleService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repository = TrainingSampleRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        return cls()

    def import_questions(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            question = str(row.get("question", "")).strip()
            category = str(row.get("category", "")).strip()

            if question:
                self.repository.save_question(question, category)

    def import_answers(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            question_text = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()

            if question_text and answer:
                self.repository.save_answer(question_text, answer)

    def get_training_data(self) -> list[dict]:
        return self.repository.get_all_samples()
