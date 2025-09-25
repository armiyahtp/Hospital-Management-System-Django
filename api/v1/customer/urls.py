from django.urls import path,include
from api.v1.customer import views



urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),





    path('departments/', views.departments, name='departments'),
    path('department/<int:id>/', views.single_department, name='single_department'),




    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:id>/', views.single_doctor, name='single_doctor'),


    
    path('testimonials/', views.testimonials, name='testimonials'),




    path('appointments/', views.all_appointments, name='all_appointments'),
    path('appointments/latest', views.latest_appointments, name='latest_appointments'),
    path('appointments/pre', views.pre_appointments, name='pre_appointments'),



    path('contact/', views.contact, name='contact'),
]
