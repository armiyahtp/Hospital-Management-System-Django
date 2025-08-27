from django.db import models
from users.models import User





class ApprovedReceptionist(models.Model):
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)



    class Meta:
        db_table = 'approved_receptionist'
        verbose_name = 'approved receptionist'
        verbose_name_plural = 'approved receptionists'
        ordering = ["-id"]


        
    def __str__(self):
        return f"{self.name} ({self.license_number})"





class Receptionist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)


    class Meta:
        db_table = 'receptionists_receptionist'
        verbose_name = 'receptionist'
        verbose_name_plural = 'receptionists'
        ordering = ["-id"]
    
    def __str__(self):
        return f"{self.user.email} ({self.license_number})"