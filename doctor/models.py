from django.db import models
from users.models import User







class DoctorsInHospital(models.Model):
    hospital = models.ForeignKey("hospital.Hospital", on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey("hospital.Department", on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


    class Meta:
        db_table = 'hospital_doctors'
        verbose_name = 'hospital doctor'
        verbose_name_plural = 'hospital doctors'
        ordering = ["-id"]

  
    def __str__(self):
        return f"{self.name} ({self.license_number}) --- {self.department.name}"















class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='doctor_image', null=True, blank=True)
    department = models.ForeignKey("hospital.Department", on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor')
    description = models.TextField(blank=True, null=True)
    experience = models.CharField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Doctor fee", null=True, blank=True)
    



    class Meta:
        db_table = 'doctors_doctor'
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'
        ordering = ["-id"]



    def __str__(self):
        return f"{self.user.email} --- {self.department.name if self.department else 'No Department'}"
    








class Leave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)


    class Meta:
        db_table = 'doctors_leave'
        verbose_name = 'leave'
        verbose_name_plural = 'leaves'
        ordering = ["-id"]



    def __str__(self):
        return self.doctor.user.email
    
