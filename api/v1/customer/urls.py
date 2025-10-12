from django.urls import path,include
from api.v1.customer import views



urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),


    path('user/me/', views.logged_user, name='logged_user'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),





    path('departments/', views.departments, name='departments'),
    path('department/<int:id>/', views.single_department, name='single_department'),




    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:id>/', views.single_doctor, name='single_doctor'),


    
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonial/add/', views.add_testimonial, name='add_testimonial'),
    path('testimonial/edit/<int:id>/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonial/delete/<int:id>/', views.delete_testimonial, name='delete_testimonial'),


    path('appointments/', views.today_appointments, name='all_appointments'),
    path('appointments/latest', views.latest_appointments, name='latest_appointments'),
    path('appointments/pre', views.pre_appointments, name='pre_appointments'),
    path('appointments/bill/<int:id>/', views.appointment_bill, name='appointment_bill'),
    path('appointments/<int:id>/', views.single_appointment, name='single_appointment'),
    path('appointments/prescription/<int:id>/', views.appointment_prescription, name='appointment_prescription'),


    path('appointment/payment/<int:id>/', views.create_payment_intent, name='create_payment_intent'),
    path('appointment/confirm/<int:id>/', views.take_appointment_after_payment, name='take_appointment_after_payment'),
    path('appointment/cancel/<int:id>/', views.intent_cancel, name='intent_cancel'),




    path('contact/', views.contact, name='contact'),
]
