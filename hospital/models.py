from django.db import models
from doctor.models import *



class Room(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=1)
    facilities = models.CharField(max_length=200)


    class Meta:
        db_table = 'hospital_rooms'
        verbose_name = 'hospital room'
        verbose_name_plural = 'hospital rooms'
        ordering = ["-id"]

    def __str__(self):
        return self.name








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
    date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='pending')
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'patient_appointments'
        verbose_name = 'patient appointment'
        verbose_name_plural = 'patient appointments'
        ordering = ["-id"]

