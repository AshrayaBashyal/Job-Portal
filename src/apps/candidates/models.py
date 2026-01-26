from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    full_name = models.CharField(max_length=150)
    skills = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.full_name