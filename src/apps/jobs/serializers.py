from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    # Use the 'get_job_type_display' method to get the human-friendly label
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "title", "description", "location", 
            "salary", "job_type", "job_type_display", "company", "company_name", "created_at"
        ]
        read_only_fields = ["id", "created_at"]
