from django.db import models
from users.models import User





class DoctorsInHospital(models.Model):
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)



    class Meta:
        db_table = 'hospital_doctors'
        verbose_name = 'hospital doctor'
        verbose_name_plural = 'hospital doctors'
        ordering = ["-id"]


        
    def __str__(self):
        return f"{self.name} ({self.license_number})"







class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)



    class Meta:
        db_table = 'doctors_doctor'
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'
        ordering = ["-id"]



    def __str__(self):
        return f"{self.user.email} ({self.license_number})"
