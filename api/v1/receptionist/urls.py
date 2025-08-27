from django.urls import path,include
from api.v1.receptionist import views



urlpatterns = [
    path('login/', views.receptionist_login, name='receptionist_login'),
    path('register/', views.receptionist_register, name='receptionist_register'),
]
