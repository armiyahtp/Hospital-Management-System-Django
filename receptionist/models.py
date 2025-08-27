from django.db import models
from users.models import User



class Receptionist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = 'receptionists_receptionist'
        verbose_name = 'receptionist'
        verbose_name_plural = 'receptionists'
        ordering = ["-id"]
    
    def __str__(self):
        return self.user.email 