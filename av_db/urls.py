"""
URL configuration for av_db project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kakao-oauth/', include('kakao_oauth.urls')),
    path('account/', include('account.urls')),
    path('account_profile/', include('account_profile.urls')),
    path('review/', include('review.urls')),
    path('google-oauth/', include('google_oauth.urls')),
    path('naver-oauth/', include('naver_oauth.urls')),
    path('company_report/',include('company_report.urls')),
    path('company_job/', include('company_job.urls')),
    path('cart/',include('cart.urls')),
    path('orders/',include('orders.urls')),
    path('marketing/',include('marketing.urls')),
    path('management/',include('management.urls')),
    path('interview/', include('interview.urls')),
    path('interview_result/', include('interview_result.urls')),
    path('interview_question_data/', include('interview_question_data.urls')),
    path('authentication/', include('authentication.urls')),
    path('github-oauth/', include('github_authentication.urls')),
    path("github-action-monitor/", include('github_action_monitor.urls')),
    path("excel-basic/", include('excel_basic.urls')),
    path('guest-oauth/', include('guest_oauth.urls')),
    path('memberships/', include('membership_plan.urls')),
    path('payments/', include('payments.urls')),
    path('training_sample/', include('training_sample.urls')),
]
