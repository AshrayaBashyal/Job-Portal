from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsEmployer


class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        user = self.request.user
        # Access companies through the reverse relationship
        return user.employer_profile.companies.all()

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer_profile)

#                 OR

# class CompanyCreateView(generics.CreateAPIView):
#     serializer_class = CompanySerializer
#     permission_classes = [IsAuthenticated, IsEmployer]

#     def perform_create(self, serializer):
#         employer_profile = self.request.user.employer_profile     # if no related_name='..' use  self.request.user.employerprofile
#         serializer.save(employer=employer_profile)


# class MyCompanyView(generics.ListAPIView):
#     serializer_class = CompanySerializer
#     permission_classes = [IsAuthenticated, IsEmployer]

#     def get_queryset(self):
#         return self.request.user.employer_profile.companies.all()




# orward Link: EmployerProfile.user --> gives you the User.
# Reverse Link: User.employer_profile --> gives you the EmployerProfile.