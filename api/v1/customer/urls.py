from django.urls import path,include
from api.v1.customer import views



urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('testimonials/', views.testimonials, name='testimonials'),
]
