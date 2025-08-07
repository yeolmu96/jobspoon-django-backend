from abc import ABC, abstractmethod
import pandas as pd

class TrainingSampleService(ABC):

    @abstractmethod
    def import_questions(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def import_answers(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def get_training_data(self) -> list[dict]:
        pass
