from abc import ABC, abstractmethod


class GithubActionMonitorRepository(ABC):

    @abstractmethod
    def getGithubActionWorkflow(self, token, repoUrl):
        pass

    @abstractmethod
    def triggerGithubActionWorkflow(self, token: str, repoUrl: str, workflowName: str):
        pass