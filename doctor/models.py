from django.db import models
from users.models import User




class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='doctor_image', null=True, blank=True)
    department = models.ForeignKey("hospital.Department", on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor')
    description = models.TextField(blank=True, null=True)
    experience = models.IntegerField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Doctor fee", null=True, blank=True)
    



    class Meta:
        db_table = 'doctors_doctor'
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'
        ordering = ["-id"]



    def __str__(self):
        return self.user.email
    








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
