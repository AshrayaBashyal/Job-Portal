from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Job
from .serializers import JobSerializer
from apps.companies.models import Company
from apps.companies.permissions import IsEmployer


class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        # company_id = self.request.data.get("company")

        # try:
        #     company = Company.objects.get(id=company_id)        # company = get_object_or_404(Company, id=company_id)
        # except Company.DoesNotExist:
        #     raise PermissionDenied("Invalid company.")

        company = serializer.validated_data.get("company")

        if company.employer.user != self.request.user:
            raise PermissionDenied("You do not own this company.")

        serializer.save(company=company)


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [AllowAny]


class MyJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(company__employer__user=self.request.user)
