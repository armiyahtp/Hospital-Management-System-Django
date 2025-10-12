from django.db import models
from datetime import datetime, timedelta, date
from django.utils import timezone
from doctor.models import Doctor
from customer.models import Customer
import datetime
import random
import string
import math







class Hospital(models.Model):
    logo = models.FileField(upload_to='hospital_logo')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    class Meta:
        db_table = 'hospital_details'
        verbose_name = 'hospital detail'
        verbose_name_plural = 'hospital details'
        ordering = ["-id"]


    def __str__(self):
        return f'{self.name} - {self.address}'









class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    logo = models.FileField(upload_to='department_logo')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        db_table = 'hospital_departments'
        verbose_name = 'hospital department'
        verbose_name_plural = 'hospital departments'
        ordering = ["-id"]


    def __str__(self):
        return self.name





    



class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'room_facilities'
        verbose_name = 'room facility'
        verbose_name_plural = 'room facilities'
        ordering = ["-id"]


    def __str__(self):
        return self.name











class Room(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    ROOM_TYPES = [
        ("PRIVATE", "Private Room"),
        ("DELUXE", "Deluxe Room"),
    ]

    room_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default="PRIVATE")
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)


    class Meta:
        db_table = 'hospital_rooms'
        verbose_name = 'hospital room'
        verbose_name_plural = 'hospital rooms'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.get_room_type_display()} - {self.room_number} ({'Occupied' if self.is_occupied else 'Available'})"















class ICU(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    ICU_TYPE_CHOICES = (
        ("MICU", "Medical ICU"), 
        ("SICU", "Surgical ICU"), 
        ("CICU", "Cardiac ICU"),     
    )
    name = models.CharField(max_length=100) 
    icu_type = models.CharField(max_length=20, choices=ICU_TYPE_CHOICES)
    floor = models.IntegerField(default=0)
    total_beds = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'hospital_icus'
        verbose_name = 'hospital icu'
        verbose_name_plural = 'hospital icus'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.get_icu_type_display()} ({self.name})"

















class ICUBed(models.Model):
    icu = models.ForeignKey(ICU, related_name="icubeds", on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    has_ventilator = models.BooleanField(default=False)
    has_monitor = models.BooleanField(default=True)
    has_oxygen_supply = models.BooleanField(default=True)

    notes = models.TextField(blank=True)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'icu_bed'
        verbose_name = 'icu bed'
        verbose_name_plural = 'icu beds'
        ordering = ["-id"]

    class Meta:
        unique_together = ("icu", "bed_number")

    def __str__(self):
        return f"{self.icu.name} - Bed {self.bed_number} ({'Available' if self.is_available else 'Occupied'})"





















class GeneralWard(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    floor = models.IntegerField(default=0)
    total_beds = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'hospital_generals'
        verbose_name = 'hospital general'
        verbose_name_plural = 'hospital generals'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.total_beds} beds"















class GeneralWardBed(models.Model):
    ward = models.ForeignKey(GeneralWard, related_name="beds", on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=10)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2) 
    has_monitor = models.BooleanField(default=True)
    has_oxygen_supply = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'general_beds'
        verbose_name = 'general bed'
        verbose_name_plural = 'general beds'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.ward.name} - Bed {self.bed_number} ({'Available' if self.is_available else 'Occupied'})"


















class DoctorsInHospital(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


    class Meta:
        db_table = 'hospital_doctors'
        verbose_name = 'hospital doctor'
        verbose_name_plural = 'hospital doctors'
        ordering = ["-id"]

  
    def __str__(self):
        return f"{self.name} ({self.license_number})"













class DoctorAvailability(models.Model):
    WEEKDAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    weekday = models.IntegerField(choices=WEEKDAYS) 
    start_time = models.TimeField() 
    end_time = models.TimeField()
    consult_duration = models.IntegerField(default=10)
    break_start = models.TimeField(blank=True, null=True)
    break_end = models.TimeField(blank=True, null=True)
        

    class Meta:
        unique_together = ("doctor", "weekday")  
        db_table = 'doctors_availability'
        verbose_name = 'doctor availability'
        verbose_name_plural = 'doctors availability'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} - {self.get_weekday_display()}"











class Token(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="tokens")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="tokens")
    appointment_date = models.DateField()
    token_number = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)


    class Meta:
        unique_together = ('doctor', 'appointment_date', 'token_number')
        db_table = 'tokens'
        verbose_name = 'token' 
        verbose_name_plural = 'tokens'
        ordering = ["-id"]
    

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} - {self.token_number} - {self.appointment_date}"












class Patient(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    phone_number = models.CharField(max_length=15)
    place = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'patients_patient'
        verbose_name = 'patient'
        verbose_name_plural = 'patients'
        ordering = ["-id"]
    

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return f"{self.first_name}" 
        return "Unknown Patient"
    














class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    )


    token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="appointments")
    token_number = models.CharField(max_length=20)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='confirmed')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    appointment_duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('doctor', 'appointment_date', 'token_number')
        db_table = 'patient_appointments'
        verbose_name = 'patient appointment'
        verbose_name_plural = 'patient appointments'
        ordering = ["-id"]


    def __str__(self):
        return self.patient.first_name + " " + self.patient.last_name + " - " + str(self.appointment_date)
    












class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="prescriptions") 
    title = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Prescription for Flu")
    notes = models.TextField(blank=True, null=True, help_text="Doctor's additional notes or instructions")
    duration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 5 days")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('patient', 'appointment')
        db_table = 'patient_prescriptions'
        verbose_name = 'patient prescription'
        verbose_name_plural = 'patient prescriptions'
        ordering = ["-id"]


    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} (Appt #{self.appointment.id})"
    
 









class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")
    medicine = models.CharField(max_length=255, null=True, blank=True)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg", null=True, blank=True)
    frequency = models.CharField(max_length=100, help_text="e.g., twice daily", null=True, blank=True)
    instructions = models.TextField(blank=True, null=True, help_text="Additional instructions if any")


    class Meta: 
        unique_together = ('prescription', 'medicine', 'dosage', 'frequency')
        db_table = 'prescription_items'
        verbose_name = ' prescription item'
        verbose_name_plural = ' prescription items'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.medicine} for {self.prescription.patient.first_name} {self.prescription.patient.last_name}"








class AdmissionRequest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name="admission_requests")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)
    preferred_icu = models.ForeignKey(ICU, null=True, blank=True, on_delete=models.SET_NULL)
    preferred_ward = models.ForeignKey(GeneralWard, null=True, blank=True, on_delete=models.SET_NULL)
    preferred_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admission_requests'
        verbose_name = 'admission request'
        verbose_name_plural = 'admission requests'
        ordering = ["-id"]

    def __str__(self):
        return f"Admission Request - {self.patient} ({self.status})"








class Admission(models.Model):
    ADMISSION_STATUS = (
        ("ADMITTED", "Admitted"),
        ("DISCHARGED", "Discharged"),
        ("CANCELLED", "Cancelled"),
    )

    patient = models.ForeignKey(Patient, related_name="admissions", on_delete=models.SET_NULL, null=True, blank=True)
    admitting_request = models.ForeignKey(AdmissionRequest, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)

    icu = models.ForeignKey(ICU, null=True, blank=True, on_delete=models.SET_NULL)
    icu_bed = models.ForeignKey(ICUBed, null=True, blank=True, on_delete=models.SET_NULL)

    ward = models.ForeignKey(GeneralWard, null=True, blank=True, on_delete=models.SET_NULL)
    ward_bed = models.ForeignKey(GeneralWardBed, null=True, blank=True, on_delete=models.SET_NULL)

    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    admit_datetime = models.DateTimeField(default=timezone.now)
    discharge_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=ADMISSION_STATUS, default="ADMITTED")
    is_emergency = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'hospital_admissions'
        verbose_name = 'hospital admission'
        verbose_name_plural = 'hospital admissions'
        ordering = ["-id"]

    def __str__(self):
        return f"Admission - {self.patient} ({self.status})"

    @property
    def stay_duration_value(self):
        end_time = self.discharge_datetime or timezone.now()
        delta = end_time - self.admit_datetime
        total_hours = delta.total_seconds() / 3600

        if total_hours < 24:
            return {"type": "hours", "value": round(total_hours, 2)}
        else:
            return {"type": "days", "value": round(total_hours / 24, 2)}



















class AppointmentBill(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointment_bills")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="bills")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    

    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicines_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tests_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    injections_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    intravenous_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surgery_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nursing_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    misc_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)   

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    bill_number = models.CharField(max_length=100, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("appointment", "bill_number")
        db_table = 'appointment_bills'
        verbose_name = 'appointment bill'
        verbose_name_plural = 'appointment bills'
        ordering = ["-id"]

    @property
    def update_totals(self):
        self.medicines_total = sum(m.total_price for m in self.medicine_items.all())
        self.tests_total = sum(t.total_price for t in self.test_items.all())
        self.injections_total = sum(i.total_price for i in self.injection_items.all())
        self.intravenous_total = sum(iv.total_price for iv in self.intravenous_items.all())
        self.room_total = sum(r.total_price for r in self.room_items.all())
        self.surgery_total = sum(s.total_price for s in self.surgery_items.all())
        self.nursing_total = sum(n.total_price for n in self.nursing_items.all())
        self.misc_total = sum(x.total_price for x in self.misc_items.all())   

        self.subtotal = (
            self.consultation_fee +
            self.medicines_total +
            self.tests_total +
            self.injections_total +
            self.intravenous_total +
            self.room_total +
            self.surgery_total +
            self.nursing_total +
            self.misc_total
        )
        net = self.subtotal - self.discount + self.tax
        self.total_amount = max(net, 0)
        self.balance_due = self.total_amount - self.amount_paid
        self.status = 'paid' if self.balance_due <= 0 else 'pending'
        self.save()

    def save(self, *args, **kwargs):
        if not self.bill_number:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.bill_number = f"BILL-{date_str}-{rand_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        patient_name = str(self.patient.first_name) if self.patient else "Unknown"
        return f"Bill {self.bill_number} - {patient_name}"









class BillMedicineItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="medicine_items")
    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'medicine_name')
        db_table = 'medicine_bills'
        verbose_name = 'medicine bill'
        verbose_name_plural = 'medicine bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals


    def __str__(self):
        return f"{self.medicine_name} x {self.quantity}"













class BillTestItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="test_items")
    test_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'test_name')
        db_table = 'test_bills'
        verbose_name = 'test bill'
        verbose_name_plural = 'test bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.test_name} x {self.quantity}"













class BillInjectionItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="injection_items")
    injection_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'injection_name')
        db_table = 'injection_bills'
        verbose_name = 'injection bill'
        verbose_name_plural = 'injection bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.injection_name} x {self.quantity}"















class BillIntravenousItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="intravenous_items")
    iv_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'iv_name')
        db_table = 'iv_bills'
        verbose_name = 'iv bill'
        verbose_name_plural = 'iv bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.iv_name} x {self.quantity}"















class BillRoomItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="room_items")
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('bill', 'admission')
        db_table = 'room_bills'
        verbose_name = 'room bill'
        verbose_name_plural = 'room bills'
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
        self.bill.update_totals()

    def calculate_total(self):
        duration = self.admission.stay_duration_value
        total = 0

        if self.admission.icu and self.admission.icu_bed:
            rate = self.admission.icu_bed.rate_per_hour
            total = duration["value"] * rate if duration["type"] == "hours" else duration["value"] * rate * 24

        elif self.admission.ward and self.admission.ward_bed:
            rate = self.admission.ward_bed.rate_per_hour
            total = duration["value"] * rate if duration["type"] == "hours" else duration["value"] * rate * 24

        elif self.admission.room:
            rate = self.admission.room.daily_rate
            if duration["type"] == "hours":
                total = math.ceil(duration["value"] / 24) * rate
            else:
                total = duration["value"] * rate

        return round(total, 2)

    def __str__(self):
        duration = self.admission.stay_duration_value
        value = f'{duration["value"]} {duration["type"]}'
        if self.admission.icu:
            return f"ICU - {value}"
        if self.admission.ward:
            return f"General Ward - {value}"
        if self.admission.room:
            return f"Room - {value}"
        return f"Admission Bill - {value}"












class BillSurgeryItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="surgery_items")
    surgery_name = models.CharField(max_length=255)
    ot_hours = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    ot_charge_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surgeon_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    anesthesia_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    class Meta:
        db_table = 'ot_bills'
        verbose_name = 'ot bill'
        verbose_name_plural = 'ot bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = (
            (self.ot_hours * self.ot_charge_per_hour) +
            self.surgeon_fee +
            self.anesthesia_fee +
            self.other_charges
        )
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.surgery_name} - {self.ot_hours}"















class BillNursingItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="nursing_items")
    nursing_care = models.CharField(max_length=255) 
    visits = models.IntegerField(default=1)  
    charge_per_visit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'nursing_care')
        db_table = 'visit_bills'
        verbose_name = 'visit bill'
        verbose_name_plural = 'visit bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.visits * self.charge_per_visit
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.nursing_care} - {self.visits} visits"
















class BillMiscItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="misc_items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    class Meta:
        unique_together = ('bill', 'description')
        db_table = 'misc_bills'
        verbose_name = 'misc bill'
        verbose_name_plural = 'misc bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.description} - {self.amount}"











class Payment(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
    )
    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )


    bill = models.OneToOneField(AppointmentBill, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_intent_id = models.CharField(max_length=255, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'bill_payments'
        verbose_name = 'bill payment'
        verbose_name_plural = 'bill payments'
        ordering = ["-id"]


    def __str__(self):
        return f"Payment for Bill #{self.bill.id} - {self.status} {self.id}"
    















class Contact(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    primary_phone = models.CharField(max_length=15)
    emergency_phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'hospital_contacts'
        verbose_name = 'hospital contact'
        verbose_name_plural = 'hospital contacts'
        ordering = ["-id"]


    def __str__(self):
        return f'{self.hospital.name} - {self.primary_phone}'
