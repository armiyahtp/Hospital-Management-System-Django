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
    










class CustomerSerializer(ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Customer
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'profile_image', 'dob', 'gender', 'place', 'address')

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
    department = DepartmentSerializer()
    class Meta:
        model = Token
        fields = ('id', 'doctor', 'department', 'appointment_date', 'token_number', 'start_time', 'end_time', 'is_booked', 'is_canceled')









class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    department = DepartmentSerializer()
    token = TokenSerializer()
    class Meta:
        model = Appointment
        fields = ('id', 'token', 'patient', 'doctor', 'department', 'token_number', 'appointment_date', 'start_time', 'end_time', 'status', 'reason', 'notes', 'appointment_duration')










class PrescriptionItemSerializer(ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ('id', 'medicine', 'dosage', 'frequency', 'instructions')






class PrescriptionSerializer(ModelSerializer):
    appointment = AppointmentSerializer()
    items = PrescriptionItemSerializer(many=True, read_only=True)
    class Meta:
        model = Prescription
        fields = ('id', 'title', 'notes', 'duration', 'appointment', 'items', 'created_at')
        read_only_fields = ('created_at',)










class AppointmentBillSerializer(ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    appointment = AppointmentSerializer()
    class Meta:
        model = AppointmentBill
        fields = ('patient', 'doctor', 'appointment', 'consultation_fee', 'medicines_total', 'tests_total', 'injections_total', 'intravenous_total', 'room_charges_total', 'surgery_total', 'nursing_total', 'misc_total', 'subtotal', 'discount', 'tax', 'total_amount', 'amount_paid', 'balance_due', 'status', 'bill_number')













class TestimonialSerializer(ModelSerializer):
    patient = PatientSerializer()
    profile_image = serializers.ImageField(source="patient.customer.profile_image", read_only=True)
    class Meta:
        model = Testimonial
        fields = ('id', 'patient', 'service_name', 'rating', 'description', 'profile_image')














class ContactSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = Contact
        fields = ('id', 'hospital', 'primary_phone', 'emergency_phone', 'is_active')











class BillMedicineSerializer(ModelSerializer):
    class Meta:
        model = BillMedicineItem
        fields = ('id', 'medicine_name', 'quantity', 'unit_price', 'total_price')







class BillTestSerializer(ModelSerializer):
    class Meta:
        model = BillTestItem
        fields = ('id', 'test_name', 'quantity', 'unit_price', 'total_price')








class BillInjectionSerializer(ModelSerializer):
    class Meta:
        model = BillInjectionItem
        fields = ('id', 'injection_name', 'quantity', 'unit_price', 'total_price')









class BillIVSerializer(ModelSerializer):
    class Meta:
        model = BillIntravenousItem
        fields = ('id', 'iv_name', 'quantity', 'unit_price', 'total_price')







class BillRoomSerializer(ModelSerializer):
    class Meta:
        model = BillRoomItem
        fields = ('id', 'admission', 'total_price')









class BillSurgerySerializer(ModelSerializer):
    class Meta:
        model = BillSurgeryItem
        fields = ('id', 'surgery_name', 'ot_hours', 'ot_charge_per_hour', 'surgeon_fee', 'anesthesia_fee', 'other_charges', 'total_price')












class BillNursingSerializer(ModelSerializer):
    class Meta:
        model = BillNursingItem
        fields = ('id', 'nursing_care', 'visits', 'charge_per_visit', 'total_price')







class BillMiscSerializer(ModelSerializer):
    class Meta:
        model = BillMiscItem
        fields = ('id', 'description', 'quantity', 'unit_price', 'total_price')









class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'method', 'status', 'paid_amount', 'paid_at', 'transaction_id')









class AppointmentBillSerializer(ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    appointment = AppointmentSerializer()
    medicine_items = BillMedicineSerializer(many=True, read_only=True)
    test_items = BillTestSerializer(many=True, read_only=True)
    injection_items = BillInjectionSerializer(many=True, read_only=True)
    intravenous_items = BillIVSerializer(many=True, read_only=True)
    room_items = BillRoomSerializer(many=True, read_only=True)
    surgery_items = BillSurgerySerializer(many=True, read_only=True)
    nursing_items = BillNursingSerializer(many=True, read_only=True)
    misc_items = BillMiscSerializer(many=True, read_only=True)
    payment = PaymentSerializer()
    class Meta:
        model = AppointmentBill
        fields = ('id', 'patient', 'doctor', 'appointment', 'consultation_fee', 'medicines_total', 'tests_total', 'injections_total', 'intravenous_total', 'room_total', 'surgery_total', 'nursing_total', 'misc_total', 'subtotal', 'discount', 'tax', 'total_amount', 'amount_paid', 'balance_due', 'status', 'bill_number', 'medicine_items', 'test_items', 'injection_items', 'intravenous_items', 'room_items', 'surgery_items', 'nursing_items', 'misc_items', 'payment')