from abc import ABC, abstractmethod

class InterviewResultService(ABC):
    @abstractmethod
    def saveInterviewResult(self, accountId):
        pass


    @abstractmethod
    def getInterviewResult(self, userToken):
        pass

    @abstractmethod
    def getFullQAList(self, interviewId):
        pass

    @abstractmethod
    def saveQAScoreList(self, interview_result, qa_scores):
        pass

    @abstractmethod
    def recordHexagonEvaluation(self, interview_result, evaluation_scores: dict):
        pass