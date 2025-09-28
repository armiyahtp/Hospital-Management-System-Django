from django.urls import path,include
from api.v1.customer import views



urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),


    path('user/me/', views.logged_user, name='logged_user'),





    path('departments/', views.departments, name='departments'),
    path('department/<int:id>/', views.single_department, name='single_department'),




    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:id>/', views.single_doctor, name='single_doctor'),


    
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonial/add/', views.add_testimonial, name='add_testimonial'),
    path('testimonial/edit/<int:id>/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonial/delete/<int:id>/', views.delete_testimonial, name='delete_testimonial'),


    path('appointments/', views.all_appointments, name='all_appointments'),
    path('appointments/latest', views.latest_appointments, name='latest_appointments'),
    path('appointments/pre', views.pre_appointments, name='pre_appointments'),



    path('contact/', views.contact, name='contact'),
]
