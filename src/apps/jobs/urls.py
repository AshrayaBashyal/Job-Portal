from django.urls import path
from .views import JobCreateView, JobListView, MyJobsView

urlpatterns = [
    path("create/", JobCreateView.as_view()),
    path("", JobListView.as_view()),
    path("my/", MyJobsView.as_view()),
]
