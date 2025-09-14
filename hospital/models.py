from django.db import models
from doctor.models import *








class Room(models.Model):
    ROOM_TYPES = [
        ("GENERAL", "General Ward"),
        ("SEMI", "Semi-Private"),
        ("PRIVATE", "Private Room"),
        ("ICU", "ICU"),
        ("DELUXE", "Deluxe Room"),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default="GENERAL")
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)


    class Meta:
        db_table = 'hospital_rooms'
        verbose_name = 'hospital room'
        verbose_name_plural = 'hospital rooms'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.get_room_type_display()} - {self.room_number}"













class DoctorsInHospital(models.Model):
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
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
        

    class Meta:
        unique_together = ("doctor", "weekday")  
        db_table = 'doctors_availability'
        verbose_name = 'doctor availability'
        verbose_name_plural = 'doctors availability'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.doctor.name} - {self.get_weekday_display()}"











class Patient(models.Model):
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
        return f"{self.first_name} {self.last_name}"
    










class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    )


    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient  = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='pending')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'patient_appointments'
        verbose_name = 'patient appointment'
        verbose_name_plural = 'patient appointments'
        ordering = ["-id"]


    def __str__(self):
        return self.patient
    










class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="prescriptions") 
    notes = models.TextField(blank=True, null=True, help_text="Doctor's additional notes or instructions")
    duration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 5 days")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'patient_prescriptions'
        verbose_name = 'patient prescription'
        verbose_name_plural = 'patient prescriptions'
        ordering = ["-id"]


    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} (Appt #{self.appointment.id})"
    










class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")
    medicine = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., twice daily")
    instructions = models.TextField(blank=True, null=True, help_text="Additional instructions if any")


    class Meta:
        db_table = 'prescription_items'
        verbose_name = ' prescription item'
        verbose_name_plural = ' prescription items'
        ordering = ["-id"]


    def __str__(self):
        return f"{self.medicine} for {self.prescription.patient.first_name} {self.prescription.patient.last_name}"













class AppointmentBill(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointment_bills")
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
    bill_number = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'appointment_bills'
        verbose_name = 'appointment bill'
        verbose_name_plural = 'appointment bills'
        ordering = ["-id"]


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
        self.save()

    def __str__(self):
        return f"Bill {self.bill_number} - {self.patient.name}"








class BillMedicineItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="medicine_items")
    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        db_table = 'medicine_bills'
        verbose_name = 'medicine bill'
        verbose_name_plural = 'medicine bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.medicine_name} x {self.quantity}"













class BillTestItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="test_items")
    test_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
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
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    days = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        db_table = 'room_bills'
        verbose_name = 'room bill'
        verbose_name_plural = 'room bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.days * self.room.daily_rate
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.room.get_room_type_display()} - {self.days} days"















class BillSurgeryItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="surgery_items")
    surgery_name = models.CharField(max_length=255)
    surgeon_name = models.CharField(max_length=255, null=True, blank=True)
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
        return f"{self.surgery_name} - {self.surgeon_name or 'N/A'}"















class BillNursingItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="nursing_items")
    description = models.CharField(max_length=255) 
    visits = models.IntegerField(default=1)  
    charge_per_visit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    class Meta:
        db_table = 'visit_bills'
        verbose_name = 'visit bill'
        verbose_name_plural = 'visit bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.visits * self.charge_per_visit
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.description} - {self.visits} visits"
















class BillMiscItem(models.Model):
    bill = models.ForeignKey(AppointmentBill, on_delete=models.CASCADE, related_name="misc_items")
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    class Meta:
        db_table = 'misc_bills'
        verbose_name = 'misc bill'
        verbose_name_plural = 'misc bills'
        ordering = ["-id"]


    def save(self, *args, **kwargs):
        self.total_price = self.amount
        super().save(*args, **kwargs)
        self.bill.update_totals()


    def __str__(self):
        return f"{self.description} - {self.amount}"











class Payment(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
        ("insurance", "Insurance"),
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
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'bill_payments'
        verbose_name = 'bill payment'
        verbose_name_plural = 'bill payments'
        ordering = ["-id"]


    def __str__(self):
        return f"Payment for Bill #{self.bill.id} - {self.status}"