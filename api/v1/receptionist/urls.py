from django.urls import path,include
from api.v1.receptionist import views



urlpatterns = [
    path('register/', views.receptionist_register, name='receptionist_register'),


    
    path('create/doctor_availability/', views.create_doctor_availability, name='create_doctor_availability'),
    path('generate-token/', views.generate_token, name='generate_token'),
]
