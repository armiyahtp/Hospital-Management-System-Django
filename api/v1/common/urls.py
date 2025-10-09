from django.urls import path,include
from api.v1.common import views



urlpatterns = [
    path('login/', views.login, name='login'),
]
