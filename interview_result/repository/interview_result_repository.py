from abc import ABC, abstractmethod

class InterviewResultRepository(ABC):
    @abstractmethod
    def registerInterviewResult(self, account):
        pass

    @abstractmethod
    def registerInterviewResultQAS(self, interviewResult, scoreResultList):
        pass

    @abstractmethod
    def getLastInterviewResult(self,account):
        pass

    @abstractmethod
    def getLastInterviewResultQASList(self, interviewResult):
        pass

    @abstractmethod
    def saveInterviewResult(self, accountId):
        pass

    @abstractmethod
    def saveQAScoreList(self, interview_result, qa_scores):
        pass

    @abstractmethod
    def saveHexagonScore(self, interview_result, evaluation_scores: dict):
        pass