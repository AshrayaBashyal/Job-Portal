from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL    # ('accounts.User')avoids circular import errors because Django resolves the string into a model class later


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    company_name = models.CharField(max_length=150)

    def __Str__(self):
        return self.company_name


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name="companies")

    def __str__(self):
        return self.name        
