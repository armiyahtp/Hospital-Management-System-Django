from django.db import models
from users.models import User
from hospital.models import Patient



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='customer_image', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    place = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)


    class Meta:
        db_table = 'customers_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ["-id"]
    
    def __str__(self):
        return self.user.email 
    




class Testimonial(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    rating = models.FloatField()
    description = models.TextField()


    class Meta:
        db_table = 'customers_feedback'
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'
        ordering = ["-id"]
    

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'