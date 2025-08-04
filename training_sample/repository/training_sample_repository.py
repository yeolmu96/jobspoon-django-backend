from abc import ABC, abstractmethod

class TrainingSampleRepository(ABC):

    @abstractmethod
    def save_question(self, question: str, category: str):
        pass

    @abstractmethod
    def save_answer(self, question_text: str, answer: str):
        pass

    @abstractmethod
    def get_all_samples(self) -> list[dict]:
        pass
