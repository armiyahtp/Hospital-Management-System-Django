from django.urls import path,include
from api.v1.doctor import views



urlpatterns = [
    path('register/', views.doctor_register, name='doctor_register'),

    path('details/', views.user_details, name='user_details'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('update-profile/', views.update_doctor_profile, name='update_doctor_profile'),


    path('availability/', views.get_doctor_availability, name='doctor_availability'),
    path('availability/<int:id>/', views.single_doctor_availability, name='single_doctor_availability'),
    path('create-availability/', views.create_doctor_availability, name='create_doctor_availability'),
    path('update-availability/<int:id>/', views.edit_doctor_availability, name='edit_doctor_availability'),
    path('delete-availability/<int:id>/', views.delete_doctor_availability, name='delete_doctor_availability'),



    path('get-token/', views.get_token, name='get_token'),
    path('generate-token/', views.generate_token, name='generate_token'),
    path('update-token/', views.update_token, name='update_token'),



    path('appointments/pre/', views.pre_appointments, name='get_appointments'),
    path('appointments/today/', views.today_appointments, name='get_appointments'),
    path('appointments/upcoming/', views.upcoming_appointments, name='get_appointments'),
    path('appointments/<int:id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/consult/<int:id>/', views.appointment_complete, name='appointment_complete'),

    


    path('prescription/<int:id>/', views.prescription_single, name='prescription_detail'), 
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescription/patient/<int:id>/', views.prescription_patient, name='prescription_patient'),
    path('prescription/create/<int:id>/', views.prescription_create, name='prescription_create'),
    path('prescription/update/<int:id>/', views.prescription_update, name='prescription_update'),
    path('prescriptionitem/create/<int:id>/', views.prescriptionitem_create, name='prescriptionitem_create'),
    path('prescriptionitem/update/<int:id>/', views.prescriptionitem_update, name='prescriptionitem_update'),
    



    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient_detail/<int:id>/', views.patient_detail, name='patient_detail'),
]
