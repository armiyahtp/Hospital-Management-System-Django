from django.urls import path,include
from api.v1.doctor import views



urlpatterns = [
    path('login/', views.doctor_login, name='doctor_login'),
    path('register/', views.doctor_register, name='doctor_register'),
]
