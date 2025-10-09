from doctor.models import Doctor
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from hospital.models import DoctorAvailability

User = get_user_model()


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    weekday = serializers.IntegerField()
    start_time = serializers.TimeField(format="%H:%M:%S")
    end_time = serializers.TimeField(format="%H:%M:%S")
    break_start = serializers.TimeField(format="%H:%M:%S", allow_null=True, required=False)
    break_end = serializers.TimeField(format="%H:%M:%S", allow_null=True, required=False)
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = DoctorAvailability
        fields = ["id", "doctor", "weekday", "start_time", "end_time", "consult_duration", "break_start", "break_end"]

    def validate(self, attrs):
        request = self.context.get("request")
        doctor = Doctor.objects.get(user=request.user)
        weekday = attrs.get("weekday", getattr(self.instance, "weekday", None))

        
        if self.instance and self.instance.weekday == weekday:
            return attrs

        if DoctorAvailability.objects.filter(doctor=doctor, weekday=weekday).exists():
            raise serializers.ValidationError({
                "weekday": "Availability for this weekday already exists."
            })
        return attrs