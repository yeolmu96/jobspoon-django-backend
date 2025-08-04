from abc import ABC, abstractmethod


class GithubActionMonitorService(ABC):

    @abstractmethod
    def requestGithubActionWorkflow(self, token, repoUrl):
        pass

    @abstractmethod
    def triggerWorkflow(self, token: str, repoUrl: str, workflowName: str):
        pass