from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from django.contrib.auth import get_user_model

from hospital.models import *
from customer.models import Testimonial

User = get_user_model()

class CustomerRegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name',  'last_name', 'phone_number', 'password', 'confirm_password',)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    






class HospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('logo', 'name', 'address', 'city', 'postal_code', 'registration_fee', 'latitude', 'longitude', 'is_active')
    








class DepartmentSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = Department
        fields = ('hospital', 'logo', 'description', 'name')









class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('user', 'profile_image', 'department', 'availabilities', 'appointments', 'tokens')








class TestimonialSerializer(ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('patient', 'service', 'rating', 'description')














class ContactSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = Contact
        fields = ('hospital', 'primary_phone', 'emergency_phone', 'is_active')