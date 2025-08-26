from django.urls import path, include


urlpatterns = [
    path('customers/', include('api.v1.customer.urls')),
    path('doctors/', include('api.v1.doctor.urls')),
    path('receptionists/', include('api.v1.receptionist.urls')),
]