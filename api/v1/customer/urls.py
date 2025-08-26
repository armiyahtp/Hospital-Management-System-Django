from django.urls import path,include
from api.v1.customer import views



urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),
]
