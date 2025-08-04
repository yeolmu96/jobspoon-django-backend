from abc import ABC, abstractmethod

from interview.entity.interview_answer import InterviewAnswer


class InterviewAnswerRepository(ABC):

    @abstractmethod
    def save(self, interviewAnswer: InterviewAnswer) -> InterviewAnswer | None:
        pass