from django.db import models
from users.models import User
from hospital.models import Department





class ApprovedReceptionist(models.Model):
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)



    class Meta:
        db_table = 'approved_receptionist'
        verbose_name = 'approved receptionist'
        verbose_name_plural = 'approved receptionists'
        ordering = ["-id"]


        
    def __str__(self):
        return f"{self.name} ({self.license_number})"





class Receptionist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='staff_image', null=True, blank=True)
    experience = models.IntegerField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'receptionists_receptionist'
        verbose_name = 'receptionist'
        verbose_name_plural = 'receptionists'
        ordering = ["-id"]
    
    def __str__(self):
        return self.user.email