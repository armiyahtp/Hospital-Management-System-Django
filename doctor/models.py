from django.db import models
from users.models import User




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
    




class Leave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
