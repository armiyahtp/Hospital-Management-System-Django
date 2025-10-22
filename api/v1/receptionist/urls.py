from django.urls import path,include
from api.v1.receptionist import views



urlpatterns = [
    path('register/', views.receptionist_register, name='receptionist_register'),



    path('status/', views.status, name='status'),


    path('profile/', views.receptionist_profile, name='receptionist_profile'),
    path('profile/update/', views.update_receptionist_profile, name='update_receptionist_profile'),
    




    path('token/lock/<int:id>/', views.token_lock, name='token_lock'),
    path('patient/appointment/create/<int:id>/', views.patient_appointment_create, name='patient_appointment_create'),
    path('patient/bill/', views.bill_patient, name='bill_patient'),
    path('patient/appointment/take/', views.take_patient_appointment, name='take_patient_appointment'),




    path('department/', views.departments, name='department'),
    path('single_department/<int:id>/', views.single_department, name='single_department'),
    path('department/patients/<int:id>/', views.department_patients, name='department_patients'),


    path('doctors/', views.doctors, name='doctors'),
    path('single/doctor/<int:id>/', views.single_doctors, name='single_doctors'),
    path('doctor/availabilities/<int:id>/', views.get_doctor_availabilities, name='get_doctor_availabilities'),
    path('single/doctor/availability/<int:id>/', views.single_doctor_availability, name='single_doctor_availability'),
    path('create/doctor/availability/<int:id>/', views.create_doctor_availability, name='create_doctor_availability'),
    path('edit/doctor/availability/<int:id>/', views.edit_doctor_availability, name='edit_doctor_availability'),
    path('delete/doctor/availability/<int:id>/', views.delete_doctor_availability, name='delete_doctor_availability'),
    path('doctor/patients/<int:id>/', views.doctor_patients, name='doctor_patients'),
     
 



    path('tokens/<int:id>/', views.get_token, name='get_token'),
    path('generate/token/', views.generate_token, name='generate_token'),




    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('pre/appointments/', views.pre_appointments, name='pre_appointments'),
    path('today/appointments/', views.today_appointments, name='today_appointments'),
    path('upcoming/appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('single/appointment/<int:id>/', views.single_appointment, name='single_appointment'),
    path('appointment/bill/<int:id>/', views.appointment_bill, name='appointment_bill'),



    path('patients/', views.all_patients, name='all_patients'),
    path('single/patient/<int:id>/', views.single_patient, name='single_patient'),

]
