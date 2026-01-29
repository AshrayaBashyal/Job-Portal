from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    job_title = serializers.ReadOnlyField(source="job.title") # Add this for UI

    class Meta:
        model = Application
        fields = (
            "id", "job", "job_title", "candidate", 
            "status", "status_display", "applied_at"
        )
        read_only_fields = ["id", "applied_at", "status", "candidate", "status_display"]