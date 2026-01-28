from django.db import models
from apps.companies.models import Company


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        INTERNSHIP = "INTERNSHIP", "Internship"

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
