from github_action_monitor.repository.github_action_monitor_repository_impl import GithubActionMonitorRepositoryImpl
from github_action_monitor.service.github_action_monitor_service import GithubActionMonitorService


class GithubActionMonitorServiceImpl(GithubActionMonitorService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__githubActionMonitorRepository = GithubActionMonitorRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestGithubActionWorkflow(self, token, repoUrl):
        return self.__githubActionMonitorRepository.getGithubActionWorkflow(token, repoUrl)

    def triggerWorkflow(self, token: str, repoUrl: str, workflowName: str):
        return self.__githubActionMonitorRepository.triggerGithubActionWorkflow(token, repoUrl, workflowName)