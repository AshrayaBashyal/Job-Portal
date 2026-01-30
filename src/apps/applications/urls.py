from django.urls import path
from .views import ApplyToJobView, JobApplicationsView, UpdateApplicationStatusView, MyApplicationsView

urlpatterns = [
    path("apply/", ApplyToJobView.as_view()),
    path("employer/", JobApplicationsView.as_view()),
    path("update/<int:pk>/", UpdateApplicationStatusView.as_view()),
    path("my/", MyApplicationsView.as_view()),
]
