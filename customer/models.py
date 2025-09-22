from django.db import models
from users.models import User



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='customer_image', null=True, blank=True)

    class Meta:
        db_table = 'customers_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ["-id"]
    
    def __str__(self):
        return self.user.email 
    




class Testimonial(models.Model):
    patient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    rating = models.FloatField()
    description = models.TextField()


    class Meta:
        db_table = 'customers_feedback'
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'
        ordering = ["-id"]
    

    def __str__(self):
        return self.patient.user.email 