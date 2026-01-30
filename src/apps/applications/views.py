from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsCandidate
from apps.jobs.models import Job


class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        job_id = self.request.data.get("job")

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise ValidationError("Job not found.")

        candidate_profile = self.request.user.candidate_profile

        # prevent double apply (extra safety)
        if Application.objects.filter(job=job, candidate=candidate_profile).exists():
            raise ValidationError("You already applied to this job.")

        serializer.save(job=job, candidate=candidate_profile)
