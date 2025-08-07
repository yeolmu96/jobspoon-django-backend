from abc import ABC, abstractmethod


class InterviewService(ABC):

    @abstractmethod
    def createInterview(self, accountId, jobCategory, experienceLevel,projectExperience,academicBackground,techStack, companyName):
        pass

    @abstractmethod
    def listInterview(self, accountId, page, pageSize):
        pass

    @abstractmethod
    def removeInterview(self, accountId, interviewId):
        pass

    @abstractmethod
    def saveQuestion(self, interview_id: int, question: str) -> bool:
        pass

    @abstractmethod
    def saveAnswer(self, accountId: int, interviewId: int, questionId: int, answerText: str) -> bool:
        pass