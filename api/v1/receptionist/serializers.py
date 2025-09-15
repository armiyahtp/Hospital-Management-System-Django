from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from hospital.models import DoctorAvailability

User = get_user_model()


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["doctor", "weekday", "start_time", "end_time", "consult_duration", "lunch_start", "lunch_end"]