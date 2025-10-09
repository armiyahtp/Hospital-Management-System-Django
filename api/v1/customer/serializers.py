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










class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('customer', 'first_name',  'last_name', 'age', 'gender', 'phone_number', 'place')




    









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
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = Doctor
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'profile_image', 'department', 'description', 'experience', 'specialization', 'fee', 'availabilities', 'appointments', 'tokens')








class DoctorAvailabilitySerializer(ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = DoctorAvailability
        fields = ('id', 'doctor', 'weekday', 'start_time', 'end_time', 'consult_duration', 'break_start', 'break_end')









class TokenSerializer(ModelSerializer):
    doctor = DoctorSerializer()
    departemnt = DepartmentSerializer()
    class Meta:
        model = Token
        fields = ('id', 'doctor', 'departemnt', 'appointment_date', 'token_number', 'start_time', 'end_time', 'is_booked', 'is_canceled')









class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    department = DepartmentSerializer()
    token_number = TokenSerializer()
    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'department', 'token_number', 'appointment_date', 'start_time', 'end_time', 'status', 'reason', 'notes', 'appointment_duration')










class PrescriptionSerializer(ModelSerializer):
    patient = PatientSerializer()
    appointment = AppointmentSerializer()
    class Meta:
        model = Prescription
        fields = ('patient', 'appointment', 'notes', 'duration')









class PrescriptionItemSerializer(ModelSerializer):
    prescription = PrescriptionSerializer()
    class Meta:
        model = PrescriptionItem
        fields = ('prescription', 'medicine', 'dosage', 'frequency', 'instructions')










class AppointmentBillSerializer(ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    appointment = AppointmentSerializer()
    class Meta:
        model = AppointmentBill
        fields = ('patient', 'doctor', 'appointment', 'consultation_fee', 'medicines_total', 'tests_total', 'injections_total', 'intravenous_total', 'room_charges_total', 'surgery_total', 'nursing_total', 'misc_total', 'subtotal', 'discount', 'tax', 'total_amount', 'amount_paid', 'balance_due', 'status', 'bill_number')













class TestimonialSerializer(ModelSerializer):
    patient = PatientSerializer()
    class Meta:
        model = Testimonial
        fields = ('id', 'patient', 'service_name', 'rating', 'description')














class ContactSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = Contact
        fields = ('id', 'hospital', 'primary_phone', 'emergency_phone', 'is_active')