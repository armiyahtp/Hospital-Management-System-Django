from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from django.shortcuts import render
import datetime
from datetime import date, timedelta





from .serializers import *
from api.v1.common.permissions import IsReceptionist
from api.v1.common.serializers import *
from receptionist.models import *
from hospital.models import *








@api_view(['POST'])
@permission_classes([AllowAny])
def receptionist_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        license_number = request.data['license_number']

        if not ApprovedReceptionist.objects.filter(email=email, license_number=license_number).exists():
            return Response({"status_code": 6002, "message": "You are not authorized to register as a receptionist"})
        
        else:
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name'),
                phone_number=serializer.validated_data.get('phone_number'),
                password=serializer.validated_data['password'],
                is_hospital_staff=True
            )
            Receptionist.objects.create(
                user=user,
            )
            return Response({"status_code": 6000, "message": "User created successfully"})
        
    return Response({"status_code": 6001, "error": serializer.errors})













@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def status(request):
    today = date.today()

    patients_count = Patient.objects.count()
    appointments_today_count = Appointment.objects.filter(appointment_date=today).count()
    upcoming_appointments_count = Appointment.objects.filter(appointment_date__gt=today).count()
    tokens_count = Token.objects.filter(appointment_date=today, is_booked=True).count()

    data = {
        "patients": patients_count,
        "appointmentsToday": appointments_today_count,
        "upcoming": upcoming_appointments_count,
        "tokens": tokens_count,
    }

    return Response({
        "status_code": 6000,
        "data": data
    })














@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def receptionist_profile(request):
    user = request.user
    try:
        receptionist = Receptionist.objects.get(user=user)
    except Receptionist.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Receptionist not found"
        })
    serializer = ReceptionistSerializer(receptionist)
    return Response({
        "status_code": 6000,
        "receptionist": serializer.data
    })



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsReceptionist]) 
def update_receptionist_profile(request):
    user = request.user
    try:
        receptionist = Receptionist.objects.get(user=user)
    except Receptionist.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Receptionist not found"
        })
    serializer = ReceptionistSerializer(receptionist, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status_code": 6000,
            "message": "Profile updated successfully",
            "receptionist": serializer.data
        })
    return Response({"status_code": 6001, "error": serializer.errors})
















@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def token_lock(request, id):
    token = Token.objects.get(id=id)
    token.is_locked = True
    token.save()

    return Response({
        "status_code": 6000,
        "message": "Token is locked",
        "token_id": token.id,
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def patient_appointment_create(request, id):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    age = request.data.get('age')
    gender = request.data.get('gender')
    phone_number = request.data.get('phone_number')
    place = request.data.get('place')


    patient = Patient.objects.create(
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        phone_number=phone_number,
        place=place,
    )

    token = Token.objects.get(id=id)

    


    registration_fee = token.doctor.department.hospital.registration_fee or 0
    doctor_fee = token.doctor.fee or 0
    amount = registration_fee + doctor_fee
    



    bill = AppointmentBill.objects.create(
        patient=patient,
        doctor=token.doctor,
        consultation_fee=amount,
        status='pending'
    )


    


    return Response({
        "status_code": 6000,
        "message": "Patient created successfully",
        "bill_id": bill.id,
        "token_id": token.id,
        "patient_id": patient.id
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def bill_patient(request):
    bill_id = request.data.get("bill_id")
    bill = AppointmentBill.objects.get(id=bill_id)

    serializer = AppointmentBillSerializer(bill)

    return Response({
        "status_code": 6000,
        "message": "Patient bill created successfully",
        "bill": serializer.data
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def take_patient_appointment(request):
    res = request.data.get("res")
    toke_id = request.data.get("token_id")
    patient_id = request.data.get("patient_id")
    reason = request.data.get("reason", "")
    notes = request.data.get("notes", "")
    bill_id = request.data.get("bill_id")
    paid_amount = request.data.get("paid_amount", 0)




    appointment_bill = AppointmentBill.objects.get(id=bill_id)
    token = Token.objects.get(id=toke_id)
    patient = Patient.objects.get(id=patient_id)
    

    if res == 'paid':
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
        appointment_bill.amount_paid = paid_amount
        appointment_bill.update_totals
        appointment_bill.save()


        return Response({
            "status_code": 6000,
            "message": "Patient apointment created successfully",
        })
    

    elif res == 'cancelled':
        appointment_bill.delete()
        token.is_locked = False
        token.save()


        return Response({
            "status_code": 6000,
            "message": "Patient apointment not created",
        })

















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def departments(request):
    instances = Department.objects.all()

    context = {
        'request' : request
    }

    serializers = DepartmentSerializer(instances, many = True, context=context)

    return Response({'statuscode':6000, 'data':serializers.data, 'message' : 'departments listed sucessfully'})



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
@permission_classes([IsAuthenticated, IsReceptionist])
def department_patients(request, id):
    department = Department.objects.get(id=id)
    patients = (
        Patient.objects
        .filter(appointments__doctor__department=department)
        .distinct()
    )
    serializer = PatientSerializer(patients, many=True)
    return Response({
        "status_code": 6000,
        "patients": serializer.data
    })




















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def doctors(request):
    instances = Doctor.objects.all()

    context = {
        'request' : request
    }

    serializers = DoctorSerializer(instances, many=True, context=context)
    return Response({
        'status_code':6000,
        'data':serializers.data,
        'message':'doctor listed'
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def single_doctors(request, id):
    instances = Doctor.objects.get(id=id)

    context = {
        'request' : request
    }

    serializers = DoctorSerializer(instances,context=context)
    return Response({
        'status_code':6000,
        'data':serializers.data,
        'message':'doctor listed'
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def get_doctor_availabilities(request, id):
    doctor = Doctor.objects.get(id=id)
    availability = DoctorAvailability.objects.filter(doctor=doctor)
    if not availability.exists():
        return Response({
            "status_code": 404,
            "message": "Availability not found"
        })
    serializer = DoctorAvailabilitySerializer(availability, many=True)
    return Response({
        "status_code": 6000,
        "availability": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def single_doctor_availability(request, id):
    try:
        availability = DoctorAvailability.objects.get(id=id)
    except DoctorAvailability.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Availability not found"
        })
    serializer = DoctorAvailabilitySerializer(availability)
    return Response({
        "status_code": 6000,
        "availability": serializer.data
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def create_doctor_availability(request, id):
    doctor = Doctor.objects.get(id=id)
    serializer = DoctorAvailabilitySerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save(doctor=doctor)


        return Response({
            "status_code": 6000,
            "message": "Availability created successfully",
            "doctoravailability": serializer.data
        })

    return Response({"status_code": 6001, "error": serializer.errors})



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsReceptionist])
def edit_doctor_availability(request, id):
    try:
        availability = DoctorAvailability.objects.get(id=id)
    except DoctorAvailability.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Availability not found"
        })
    serializer = DoctorAvailabilitySerializer(availability, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status_code": 6000,
            "message": "Availability updated successfully",
            "availability": serializer.data
        })
    return Response({"status_code": 6001, "error": serializer.errors})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsReceptionist])
def delete_doctor_availability(request, id):
    today = date.today()
    Token.objects.filter(appointment_date__lt=today).delete()
    current_date = today + timedelta(days=1)
    end_date = today + timedelta(weeks=1)
    try:
        availability = DoctorAvailability.objects.get(id=id)
        doctor = availability.doctor
        weekday = availability.weekday
        while current_date <= end_date:
            if current_date.weekday() == weekday:
                if Token.objects.filter(doctor=doctor, appointment_date=current_date, is_booked=True).exists():
                    return Response({
                        "status_code": 6001,
                        "message": f"Cannot delete availability for {current_date} as there are booked tokens."
                    })
                else:
                    Token.objects.filter(doctor=doctor, appointment_date=current_date, is_booked=False).delete()
            current_date += timedelta(days=1)
    except DoctorAvailability.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Availability not found"
        })
    availability.delete()
    return Response({
        "status_code": 6000,
        "message": "Availability deleted successfully"
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def doctor_patients(request, id):
    doctor = Doctor.objects.get(id=id)
    patients = (
        Patient.objects
        .filter(appointments__doctor=doctor)
        .distinct()
    )
    serializer = PatientSerializer(patients, many=True)
    return Response({
        "status_code": 6000,
        "patients": serializer.data
    })

















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def get_token(request, id):
    doctor = Doctor.objects.get(id=id) 
    appointment_date = request.query_params.get('appointment_date')
    tokens = Token.objects.filter(doctor=doctor, appointment_date=appointment_date).order_by('appointment_date', 'start_time')
    booked_tokens = tokens.filter(is_booked=True).count()
    serializer = TokenSerializer(tokens, many=True)

    return Response({
        "status_code": 6000,
        "tokens": serializer.data, 
        "booked_tokens": booked_tokens 
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def generate_token(request):
    availability = request.data.get('availability')
    today = date.today()

    doctor = Doctor.objects.get(id=availability['doctor'])

    Token.objects.filter(appointment_date__lt=today, doctor=doctor).delete()

    current_date = today + timedelta(days=1)
    end_date = today + timedelta(weeks=1)
    created_tokens = []

    
    while current_date <= end_date: 
        if current_date.weekday() == availability['weekday']:

            if Token.objects.filter(appointment_date=current_date).exists():
                break
            start_time = datetime.datetime.strptime(availability['start_time'], '%H:%M:%S').time()
            end_time = datetime.datetime.strptime(availability['end_time'], '%H:%M:%S').time()
            duration = availability['consult_duration']
            tkn = 1

            
            break_start = (
                datetime.datetime.strptime(availability['break_start'], '%H:%M:%S').time()
                if availability.get('break_start') else None
            )

            break_end = (
                datetime.datetime.strptime(availability['break_end'], '%H:%M:%S').time()
                if availability.get('break_end') else None
            )

            current_start_time = start_time
            
            while current_start_time < end_time:
                current_datetime = datetime.datetime.combine(current_date, current_start_time)
                if break_start and break_end:
                    break_start_datetime = datetime.datetime.combine(current_date, break_start)
                    break_end_datetime = datetime.datetime.combine(current_date, break_end)

                    if break_start_datetime <= current_datetime < break_end_datetime:
                        current_start_time = break_end
                        continue

                slot_end_datetime = current_datetime + timedelta(minutes=duration)
                slot_end_time = slot_end_datetime.time()
                
                
                if slot_end_time > end_time:
                    break
                

                
                doctor_id=availability['doctor']
                doctor = Doctor.objects.get(id=doctor_id)
                formatted = f"TKN{tkn:02d}"
                token, created = Token.objects.get_or_create(
                    doctor=doctor,
                    department=doctor.department,
                    appointment_date=current_date,
                    token_number=formatted,
                    defaults={
                        "start_time": current_start_time,
                        "end_time": slot_end_time,
                        "is_booked": False, 
                        "is_canceled": False,
                    }
                )
                if created:
                    created_tokens.append(token.id)

                
                current_start_time = slot_end_time
                tkn += 1
                
        current_date += timedelta(days=1)

    return Response({
        "status_code": 6000,
        "message": "Tokens generated successfully",
        "tokens": created_tokens,
    })


        















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def patient_appointments(request):
    pid = request.query_params.get('ptId')
    did = request.query_params.get('drId')

    if did:
        try:
            doctor = Doctor.objects.get(id=did)
            patient = Patient.objects.get(id=pid)
        except Doctor.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Doctor not found"
            })
        appointments = Appointment.objects.filter(doctor=doctor, patient=patient).order_by('-appointment_date', '-start_time')

    else:
        try:
            patient = Patient.objects.get(id=pid)
        except Patient.DoesNotExist:
            return Response({
                "status_code": 404,
            "message": "Patient not found"
        })
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-start_time')


    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def pre_appointments(request):
    pid = request.query_params.get('ptId')
    did = request.query_params.get('drId')

    if did:
        try:
            doctor = Doctor.objects.get(id=did)
            patient = Patient.objects.get(id=pid)
        except Doctor.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Doctor not found"
            })
        appointments = Appointment.objects.filter(doctor=doctor, patient=patient, appointment_date__lt=date.today()).order_by('-appointment_date', '-start_time')

    else:
        try:
            patient = Patient.objects.get(id=pid)
        except Patient.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Patient not found"
            })
        appointments = Appointment.objects.filter(patient=patient, appointment_date__lt=date.today()).order_by('-appointment_date', '-start_time')

    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def today_appointments(request):
    pid = request.query_params.get('ptId')
    did = request.query_params.get('drId')
    if did:
        try:
            doctor = Doctor.objects.get(id=did)
            patient = Patient.objects.get(id=pid)
        except Doctor.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Doctor not found"
            })
        appointments = Appointment.objects.filter(doctor=doctor, patient=patient, appointment_date=date.today()).order_by('-start_time')

    else:
        try:
            patient = Patient.objects.get(id=pid)
        except Patient.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Patient not found"
            })
        appointments = Appointment.objects.filter(patient=patient, appointment_date=date.today()).order_by('-start_time')
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def upcoming_appointments(request):
    pid = request.query_params.get('ptId')
    did = request.query_params.get('drId')
    if did:
        try:
            doctor = Doctor.objects.get(id=did)
            patient = Patient.objects.get(id=pid)
        except Doctor.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Doctor not found"
            })
        appointments = Appointment.objects.filter(doctor=doctor, patient=patient, appointment_date__gt=date.today()).order_by('appointment_date', 'start_time')

    else:
        try:
            patient = Patient.objects.get(id=pid)
        except Patient.DoesNotExist:
            return Response({
                "status_code": 404,
                "message": "Patient not found"
            })
        appointments = Appointment.objects.filter(patient=patient, appointment_date__gt=date.today()).order_by('appointment_date', 'start_time')

    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })

 

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def single_appointment(request, id):
    context = {
        "request": request
    }
    try:
        appointment = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })
    serializer = AppointmentSerializer(appointment, context=context)
    return Response({
        "status_code": 6000,
        "appointment": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def appointment_bill(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
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
@permission_classes([IsAuthenticated, IsReceptionist])
def all_patients(request):
    patients = (
        Patient.objects
        .all()
        .distinct()
    )
    serializer = PatientSerializer(patients, many=True)
    return Response({
        "status_code": 6000,
        "patients": serializer.data
    }) 



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsReceptionist])
def single_patient(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Patient not found"
        })
    serializer = PatientSerializer(patient)
    return Response({
        "status_code": 6000,
        "patient": serializer.data
    })