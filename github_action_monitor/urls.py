from django.urls import path, include
from rest_framework.routers import DefaultRouter
from github_action_monitor.controller.github_action_monitor_controller import GithubActionMonitorController

router = DefaultRouter()
router.register(r'github-action-monitor', GithubActionMonitorController, basename='github-action-monitor')

urlpatterns = [
    path('', include(router.urls)),
    path('workflow',
         GithubActionMonitorController.as_view({ 'post': 'requestGithubActionWorkflow' }),
         name='Github Action Workflow 모니터링'),
    path('trigger',
         GithubActionMonitorController.as_view({'post': 'triggerWorkflow'}),
         name='Github Action Workflow 실행')
]