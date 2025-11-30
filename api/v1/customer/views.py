from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


import stripe
from django.utils import timezone
from decimal import Decimal

import datetime
from datetime import date


from django.contrib.auth import authenticate
from .serializers import *
from api.v1.common.serializers import UserSerializer
from customer.models import *
from hospital.models import *



stripe.api_key = settings.STRIPE_SECRET_KEY





@api_view(['POST'])
@permission_classes([AllowAny])
def customer_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user and user.is_customer:
        refresh = RefreshToken.for_user(user)
        data = {
            'access' : str(refresh.access_token),
            'user' : UserSerializer(user, context = {'request' : request}).data
        }

        return Response({'status_code' : 6000, 'data' : data, 'message' : 'Login Success full'})
    return Response({'status_code' : 6001, 'error' : 'Invalid credentials'})



@api_view(['POST'])
@permission_classes([AllowAny])
def customer_register(request):
    serializer = CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            phone_number=serializer.validated_data.get('phone_number'),
            password=serializer.validated_data['password'],
            is_customer=True
        )

        dob_str = request.data.get('date_of_birth')
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
        gender = request.data.get('gender')
        place = request.data.get('place')
        address = request.data.get('address')
        Customer.objects.create(
            user=user,
            dob=dob,
            gender=gender,
            place=place,
            address=address,
        )
        refresh = RefreshToken.for_user(user)
        return Response({"status_code": 6000, 'access' : str(refresh.access_token), "message": "User created successfully"})
    return Response({"status_code": 6001, "error": serializer.errors})













@api_view(['GET'])
@permission_classes([AllowAny])
def logged_user(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    customer_id = customer.id

    return Response({'statuscode':6000, 'customer_id':customer_id, 'message' : 'user and customer id listed sucessfully'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    context = {
        'request' : request
    }

    serializer = CustomerSerializer(customer, context=context)
    return Response({'status_code': 6000, 'data': serializer.data, 'message': 'Profile retrieved successfully'})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    serializer = CustomerSerializer(customer, data=request.data, context={"request": request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status_code': 6000, 'data': serializer.data, 'message': 'Profile updated successfully'})
    return Response({'status_code': 6001, 'error': serializer.errors})

















@api_view(['GET'])
@permission_classes([AllowAny])
def departments(request):
    instances = Department.objects.all()

    context = {
        'request' : request
    }


    serializers = DepartmentSerializer(instances, many = True, context=context)

    return Response({'statuscode':6000, 'data':serializers.data, 'message' : 'departments listed sucessfully'})











@api_view(['GET'])
@permission_classes([AllowAny])
def doctors(request):
    instances = Doctor.objects.all()
    departments = Department.objects.all()


    context = {
        'request' : request
    }

    serializers = DoctorSerializer(instances, many=True, context=context)
    department_serializers = DepartmentSerializer(departments, many=True, context=context)

    return Response({
        'status_code':6000,
        'data':serializers.data, 
        'departments': department_serializers.data,
        'message':'doctor listed'
    })













@api_view(['GET'])
@permission_classes([AllowAny])
def testimonials(request):
    instances = Testimonial.objects.all()

    context = {
        'request' : request
    }

    serializers = TestimonialSerializer(instances, many=True, context=context)

    return Response({'status_code':6000, 'data':serializers.data, 'message':'testimonial listed'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_testimonial(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)


    service_name = request.data.get('service_name')
    rating = request.data.get('rating')
    description = request.data.get('description')

    Testimonial.objects.create(
        patient=patient,
        service_name=service_name,
        rating=rating,
        description=description
    )

    return Response({'status_code':6000, 'message':'testimonial added'})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_testimonial(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)


    service_name = request.data.get('service_name')
    rating = request.data.get('rating')
    description = request.data.get('description')

    testimonial = Testimonial.objects.get(id=id, patient=patient)
    testimonial.service_name = service_name
    testimonial.rating = rating
    testimonial.description = description
    testimonial.save()

    return Response({'status_code':6000, 'message':'testimonial updated'})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_testimonial(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)

    testimonial = Testimonial.objects.get(id=id, patient=patient)
    testimonial.delete()

    return Response({'status_code':6000, 'message':'testimonial deleted'})













@api_view(['GET'])
@permission_classes([AllowAny])
def contact(request):
    instance = Contact.objects.all().first()

    context = {
        "request": request
    }

    serializers = ContactSerializer(instance, context=context)

    return Response({
        "stats_code":6000,
        "data": serializers.data
    })










@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_department(request, id):
    instance = Department.objects.get(id=id)
    doctors = Doctor.objects.filter(department=instance)

    context = {
        "request": request
    }

    department_serializer = DepartmentSerializer(instance, context=context)
    doctor_serializer = DoctorSerializer(doctors, many=True, context=context)

    return Response({
        'status_code': 6000,
        'department': department_serializer.data,
        'doctors': doctor_serializer.data, 
    })











@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_doctor(request, id):
    
    instance = Doctor.objects.get(id=id)
    
    context = {"request": request}
    serializer = DoctorSerializer(instance, context=context)

    available_dates = Token.objects.filter(
        doctor=instance,
        is_booked=False,
        is_canceled=False,
        appointment_date__gte=date.today()
    ).values_list("appointment_date", flat=True).distinct().order_by("appointment_date")

    response_data = {
        "status_code": 6000,
        "doctor": serializer.data,
        "available_dates": available_dates
    }

    appointment_date_str = request.query_params.get("appointment_date")
    if appointment_date_str:
        try:
            appointment_date = datetime.datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format, expected YYYY-MM-DD"}, status=400)
        tokens = Token.objects.filter(
            doctor=instance,
            appointment_date=appointment_date,
            is_booked=False,
            is_canceled=False
        ).order_by("start_time")

        token_data = [
            {
                "id": t.id,
                "token_number": t.token_number,
                "start_time": t.start_time,
                "end_time": t.end_time,
                "is_booked": t.is_booked,
                "is_canceled": t.is_canceled,

            }
            for t in tokens
        ]
        response_data["tokens"] = token_data

    return Response({
        "status_code": 6000,
        "data": response_data
    })

































@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request,id):
    user = request.user
    customer = Customer.objects.get(user=user)
    token = Token.objects.get(id=id)
    token_date = token.appointment_date

    if Patient.objects.filter(customer=customer).exists():
        patient = Patient.objects.get(customer=customer)
        appointment = Appointment.objects.filter(
            patient=patient,
            appointment_date=token_date
        )
        
    if appointment.exists():
        return Response({"error": "You already have an appointment on this date"}, status=400)

    else:
        try:
            registration_fee = token.doctor.department.hospital.registration_fee or 0
            doctor_fee = token.doctor.fee or 0
            amount = registration_fee + doctor_fee

            bill = AppointmentBill.objects.create(
                consultation_fee=amount,
            )

            payment = Payment.objects.create(
                bill=bill,
                method="card",
            )

            
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency="usd",
                payment_method_types=["card"],
            )

            payment.stripe_intent_id = intent.id
            payment.save()

            return Response({"clientSecret": intent.client_secret, "payment_id": payment.id})
        except Exception as e:
            return Response({"error": str(e)}, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def take_appointment_after_payment(request, id):
    payment_id = request.data.get("payment_id")
    payment_intent_id = request.data.get("payment_intent_id")

    if not payment_id or not payment_intent_id:
        return Response({"error": "Payment ID and Payment Intent ID are required"}, status=400)

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        payment = Payment.objects.get(id=payment_id)

        if intent.status != "succeeded" and not settings.DEBUG:
            payment.status = "failed"
            payment.save()
            return Response({"error": "Payment not completed"}, status=400)
            

        payment.status = "completed"
        payment.transaction_id = payment_intent_id
        payment.paid_amount = Decimal(intent.amount_received) / Decimal('100') if intent.amount_received else Decimal('0')
        payment.paid_at = timezone.now()
        payment.save()


        user = request.user
        customer = Customer.objects.get(user=user)
        token = Token.objects.get(id=id)
        bill_id = payment.bill.id
        appointment_bill = AppointmentBill.objects.get(id=bill_id)

        today = date.today()
        age = today.year - customer.dob.year - (
            (today.month, today.day) < (customer.dob.month, customer.dob.day)
        )

        try:
            patient = Patient.objects.get(customer=customer)
        except Patient.DoesNotExist:
            patient = Patient.objects.create(
                customer=customer,
                first_name=user.first_name,
                last_name=user.last_name,
                age=age,
                gender=customer.gender,
                phone_number=user.phone_number,
                place=customer.place
            )


        reason = request.data.get("reason", "")
        notes = request.data.get("notes", "")
        appointment = Appointment.objects.create(
            token=token,
            patient=patient,
            doctor=token.doctor,
            department=token.department,
            token_number=token.token_number,
            appointment_date=token.appointment_date,
            start_time=token.start_time,
            end_time=token.end_time,
            reason=reason,
            notes=notes,
            status="confirmed"
        )

        token.is_booked = True 
        token.save()

        appointment_bill.patient = patient
        appointment_bill.doctor = token.doctor
        appointment_bill.appointment = appointment
        appointment_bill.amount_paid = payment.paid_amount
        appointment_bill.update_totals
        appointment_bill.save()

        return Response({
            "status_code": 6000,
            "message": "Payment successful & Appointment booked!",
            "appointment_id": appointment.id
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def intent_cancel(request, id):
    payment = Payment.objects.get(id=id)
    bill = payment.bill
    bill.delete()
    try:
        if payment.stripe_intent_id:
            stripe.PaymentIntent.cancel(payment.stripe_intent_id)
        return Response({"status": "canceled", "intent": payment.stripe_intent_id})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


























@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_appointments(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)

    today = date.today()
    appointments = Appointment.objects.filter(patient=patient, appointment_date=today).order_by('-appointment_date', '-start_time')

    serializers = AppointmentSerializer(appointments, many=True)
    result = serializers.data

    return Response({
        "status_code": 6000,
        "all_appointments": result
    })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_appointments(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)

    today = date.today()

    appointments = Appointment.objects.filter(patient=patient, appointment_date__gte=today).order_by('-appointment_date', '-start_time')
    serializers = AppointmentSerializer(appointments, many=True)


    return Response({
        "status_code": 6000,
        "latest_appointment": serializers.data,
    })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pre_appointments(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    patient = Patient.objects.get(customer=customer)

    today = date.today()

    appointments = Appointment.objects.filter(patient=patient, appointment_date__lt=today).order_by('-appointment_date', '-start_time')
    previous = AppointmentSerializer(appointments, many=True)

    return Response({
        "status_code": 6000,
        "pre_appointment": previous.data,
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_bill(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    try:
        patient = Patient.objects.get(customer=customer)
        appointment = Appointment.objects.get(id=id, patient=patient)
        appointment_bill = AppointmentBill.objects.get(appointment=appointment)
    except (Patient.DoesNotExist, Appointment.DoesNotExist):
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })

    serializer = AppointmentBillSerializer(appointment_bill)
    return Response({
        "status_code": 6000,
        "appointment_bill": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_appointment(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    try:
        patient = Patient.objects.get(customer=customer)
        appointment = Appointment.objects.get(id=id, patient=patient)
    except (Patient.DoesNotExist, Appointment.DoesNotExist):
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })
    serializer = AppointmentSerializer(appointment)
    return Response({
        "status_code": 6000,
        "appointment": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_prescription(request, id):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        patient = Patient.objects.get(customer=customer)
    except (Customer.DoesNotExist, Patient.DoesNotExist):
        return Response({
            "status_code": 404,
            "message": "Patient not found"
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        appointment_complete = Appointment.objects.get(id=id, status='completed')
    except Appointment.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Completed appointment not found"
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        prescription = Prescription.objects.get(patient=patient, appointment=appointment_complete)
    except Prescription.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Prescription not found for this appointment"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = PrescriptionSerializer(prescription)
    return Response({
        "status_code": 6000,
        "prescriptions": serializer.data
    }, status=status.HTTP_200_OK)
