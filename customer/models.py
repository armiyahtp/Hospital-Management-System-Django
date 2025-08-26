from django.db import models
from users.models import User



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = 'customers_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ["-id"]
    
    def __str__(self):
        return self.user.email 