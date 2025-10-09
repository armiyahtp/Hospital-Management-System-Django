from doctor.models import Doctor
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from hospital.models import Appointment, Department, Hospital, Patient, PrescriptionItem, Prescription


from django.contrib.auth import get_user_model

User = get_user_model()






class HospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('logo', 'name', 'address', 'city', 'postal_code', 'registration_fee', 'latitude', 'longitude', 'is_active')








class DepartmentSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = Department
        fields = ('id', 'hospital', 'logo', 'description', 'name')








class DoctorSerializer(ModelSerializer):
    department = DepartmentSerializer()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Doctor
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'profile_image', 'department', 'description', 'experience', 'specialization', 'fee')

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        
        if user_data:
            instance.user.first_name = user_data.get("first_name", instance.user.first_name)
            instance.user.last_name = user_data.get("last_name", instance.user.last_name)
            instance.user.phone_number = user_data.get("phone_number", instance.user.phone_number)
            instance.user.save()

        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance 












class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'customer', 'first_name',  'last_name', 'age', 'gender', 'phone_number', 'place')




class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer()
    class Meta:
        model = Appointment
        fields = ["id", "patient", "token_number", "appointment_date", "start_time", "end_time", "status", "reason", "notes"]





class PrescriptionItemSerializer(ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ('id', 'medicine', 'dosage', 'frequency', 'instructions')






class PrescriptionSerializer(ModelSerializer):
    appointment = AppointmentSerializer()
    items = PrescriptionItemSerializer(many=True, read_only=True)
    class Meta:
        model = Prescription
        fields = ('id', 'title', 'notes', 'duration', 'appointment', 'items')









