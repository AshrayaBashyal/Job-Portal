from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer
from .permissions import IsCandidate
from apps.companies.permissions import IsEmployer
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


class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        # if self.request.user.role != "EMPLOYER":
        #     raise PermissionDenied("Only employers can view applications.")
        # return Application.objects.filter(job__company__employer__user=user)

        return Application.objects.filter(
            job__company__employer__user=self.request.user
        ).select_related('job', 'candidate__user') 
    

class UpdateApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer] 
    serializer_class = ApplicationStatusUpdateSerializer

    def patch(self, request, pk):
        try:
            application = Application.objects.select_related('job__company__employer').get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=404)

        if application.job.company.employer.user != request.user:
            raise PermissionDenied("This application does not belong to your job postings.")

        new_status = request.data.get("status")

        if new_status not in Application.Status.values:
            return Response({"error": f"Invalid status. Choose from: {Application.Status.values}"}, status=400)

        application.status = new_status
        application.save()

        return Response({
            "message": "Status updated successfully.",
            "new_status": application.get_status_display() 
        })    