from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Max
from api.v1.common.permissions import IsDoctor



from api.v1.common.serializers import *
from doctor.models import *
from hospital.models import *
from datetime import datetime, date, timedelta
from api.v1.receptionist.serializers import DoctorAvailabilitySerializer
from .serializers import *
from customer.models import Testimonial
from api.v1.customer.serializers import TokenSerializer





@api_view(['POST'])
@permission_classes([AllowAny])
def doctor_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        license_number = request.data['license_number']

        if not DoctorsInHospital.objects.filter(email=email, license_number=license_number).exists():
            return Response({"status_code": 6002, "message": "You are not authorized to register as a doctor"})
        
        else:
            department = DoctorsInHospital.objects.get(email=email).department
            
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name'),
                phone_number=serializer.validated_data.get('phone_number'),
                password=serializer.validated_data['password'],
                is_doctor=True
            )
            Doctor.objects.create(
                user=user,
                department=department
            )
            return Response({"status_code": 6000, "message": "User created successfully"})
        
    return Response({"status_code": 6001, "error": serializer.errors})


















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def user_details(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    profile_image = doctor.profile_image

    image_url = request.build_absolute_uri(profile_image.url) if profile_image else None

    
    appointments = Appointment.objects.filter(doctor=doctor)

    earnings = sum(appointment.doctor.fee for appointment in appointments if appointment.status == 'completed')
    this_month_appointments = appointments.filter(appointment_date__month=date.today().month, status='completed').count()
    total_patients = appointments.values('patient').distinct().count()
    rating = Testimonial.objects.filter(doctor=doctor).aggregate(models.Sum('rating'))['rating__sum'] or 0.0
    rating_count = Testimonial.objects.filter(doctor=doctor).count()

    return Response({
        "status_code": 6000,
        "data": {
            "profile": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "profile_image": image_url,
            },
            "status": {
                "this_month": this_month_appointments,
                "total_patients": total_patients,
                "earnings": earnings,
                "rating": rating,
                "rating_count": rating_count
            },
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def doctor_profile(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)

    context = {
        "request": request
    }
    serializer = DoctorSerializer(doctor, context=context)
    return Response({
        "status_code": 6000,
        "doctor": serializer.data
    })



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_doctor_profile(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)

    serializer = DoctorSerializer(doctor, data=request.data, context={"request": request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code": 6000, "doctor": serializer.data})
    return Response({"status_code": 6001, "errors": serializer.errors})

















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def get_doctor_availability(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
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
@permission_classes([IsAuthenticated, IsDoctor])
def single_doctor_availability(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    try:
        availability = DoctorAvailability.objects.get(id=id, doctor=doctor)
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
@permission_classes([IsAuthenticated, IsDoctor])
def create_doctor_availability(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    serializer = DoctorAvailabilitySerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        availability = serializer.save(doctor=doctor)


        return Response({
            "status_code": 6000,
            "message": "Availability created successfully",
            "doctoravailability": serializer.data
        })

    return Response({"status_code": 6001, "error": serializer.errors})



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def edit_doctor_availability(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    try:
        availability = DoctorAvailability.objects.get(id=id, doctor=doctor)
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
@permission_classes([IsAuthenticated, IsDoctor])
def delete_doctor_availability(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    today = date.today()
    Token.objects.filter(appointment_date__lt=today).delete()
    current_date = today + timedelta(days=1)
    end_date = today + timedelta(weeks=1)
    try:
        availability = DoctorAvailability.objects.get(id=id, doctor=doctor)
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
@permission_classes([IsAuthenticated, IsDoctor])
def get_token(request):
    user = request.user
    doctor = Doctor.objects.get(user=user) 
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
@permission_classes([IsAuthenticated, IsDoctor])
def generate_token(request):
    availability = request.data.get('availability')
    today = date.today()

    Token.objects.filter(appointment_date__lt=today).delete()

    current_date = today + timedelta(days=1)
    end_date = today + timedelta(weeks=1)
    created_tokens = []

    
    while current_date <= end_date:
        if current_date.weekday() == availability['weekday']:

            if Token.objects.filter(appointment_date=current_date).exists():
                break
            start_time = datetime.strptime(availability['start_time'], '%H:%M:%S').time()
            end_time = datetime.strptime(availability['end_time'], '%H:%M:%S').time()
            duration = availability['consult_duration']
            tkn = 1

            
            break_start = (
                datetime.strptime(availability['break_start'], '%H:%M:%S').time()
                if availability.get('break_start') else None
            )

            break_end = (
                datetime.strptime(availability['break_end'], '%H:%M:%S').time()
                if availability.get('break_end') else None
            )

            current_start_time = start_time
            
            while current_start_time < end_time:
                current_datetime = datetime.combine(current_date, current_start_time)
                if break_start and break_end:
                    break_start_datetime = datetime.combine(current_date, break_start)
                    break_end_datetime = datetime.combine(current_date, break_end)
                    
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
                    departemnt=doctor.department,
                    appointment_date=current_date,
                    token_number=formatted,
                    defaults={
                        "start_time": current_start_time,
                        "end_time": slot_end_time,
                        "is_booked": False, 
                        "is_canceled": False,
                    }
                )
                aptdate = token.appointment_date
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



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_token(request):
    availability = request.data.get("availability")
    if not availability:
        return Response({"error": "Missing availability"}, status=400)

    doctor_id = availability["doctor"]
    weekday = int(availability["weekday"])
    old_start = datetime.strptime(availability["start_time"], "%H:%M:%S").time()
    old_end = datetime.strptime(availability["end_time"], "%H:%M:%S").time()
    old_duration = int(availability["consult_duration"])

    new_start_str = request.data.get("new_start_time", availability["start_time"])
    new_end_str = request.data.get("new_end_time", availability["end_time"])
    new_duration = int(request.data.get("new_consult_duration", old_duration))
    doctor_id = availability["doctor"]
    weekday = int(availability["weekday"])
    old_start = datetime.strptime(availability["start_time"], "%H:%M:%S").time()
    old_end = datetime.strptime(availability["end_time"], "%H:%M:%S").time()
    old_duration = int(availability["consult_duration"])

    
    new_start_str = request.data.get("new_start_time", availability["start_time"])
    new_end_str = request.data.get("new_end_time", availability["end_time"])
    new_duration = int(request.data.get("new_consult_duration", old_duration))

    new_start = datetime.strptime(new_start_str, "%H:%M:%S").time()
    new_end = datetime.strptime(new_end_str, "%H:%M:%S").time()

    today = date.today()
    start_date = today + timedelta(days=1)
    end_date = today + timedelta(weeks=1)

    created_tokens = []
    errors = []

    d = start_date
    while d <= end_date:
        if d.weekday() != weekday: 
            d += timedelta(days=1)
            continue

        tokens = list(Token.objects.filter(doctor_id=doctor_id, appointment_date=d).order_by("start_time"))
        first_token = tokens[0]
        last_token = tokens[-1]
        booked_tokens = [t for t in tokens if t.is_booked]
        total_tokens = len(tokens)
        booked_count = len(booked_tokens)

        
        def to_minutes(t):
            return t.hour * 60 + t.minute

        
        if first_token.is_booked:
            if to_minutes(new_start) > to_minutes(old_start):
                errors.append(f"{d}: Cannot move start time later because first token is booked.")

        
        if last_token.is_booked:
            if to_minutes(new_end) < to_minutes(old_end):
                errors.append(f"{d}: Cannot move end time earlier because last token is booked.")

        
        if not first_token.is_booked and booked_tokens:
            first_booked_start = booked_tokens[0].start_time
            if to_minutes(new_start) >= to_minutes(first_booked_start):
                errors.append(f"{d}: new_start_time cannot go beyond first booked slot {first_booked_start}.")

        
        if not last_token.is_booked and booked_tokens:
            last_booked_start = booked_tokens[-1].start_time
            if to_minutes(new_end) <= to_minutes(last_booked_start):
                errors.append(f"{d}: new_end_time cannot go before last booked slot {last_booked_start}.")

        
        if new_duration > old_duration:
            total_duration = total_tokens * old_duration
            new_token_count = total_duration // new_duration
            if booked_count > new_token_count:
                errors.append(f"{d}: Cannot increase duration to {new_duration} minutes — too many booked slots.")

        
        if errors:
            break

        
        Token.objects.filter(doctor_id=doctor_id, appointment_date=d, is_booked=False).delete()

        
        current_time = new_start
        tkn_no = 1

        while datetime.combine(d, current_time) < datetime.combine(d, new_end):
            slot_end = (datetime.combine(d, current_time) + timedelta(minutes=new_duration)).time()
            if slot_end > new_end:
                break


            overlap = any(b.start_time <= current_time < b.end_time for b in booked_tokens)
            if overlap:
                current_time = slot_end
                continue

            token_no = f"TKN{tkn_no:02d}"
            Token.objects.get_or_create(
                doctor_id=doctor_id,
                departemnt_id=first_token.departemnt_id,
                appointment_date=d,
                token_number=token_no,
                defaults={
                    "start_time": current_time,
                    "end_time": slot_end,
                    "is_booked": False,
                }
            )
            created_tokens.append(token_no)
            current_time = slot_end
            tkn_no += 1


    if errors:
        return Response({
            "status": 4001,
            "message": "Cannot update due to booking rules",
            "errors": errors
        }, status=400)

    return Response({
        "status": 6000,
        "message": "Tokens updated successfully",
        "created_tokens": created_tokens
    })





















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def pre_appointments(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointments = Appointment.objects.filter(doctor=doctor, appointment_date__lt=date.today()).order_by('-appointment_date', '-start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def today_appointments(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)

    appointments = Appointment.objects.filter(doctor=doctor, appointment_date=date.today()).order_by('-start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def upcoming_appointments(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointments = Appointment.objects.filter(doctor=doctor, appointment_date__gt=date.today()).order_by('appointment_date', 'start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        "status_code": 6000,
        "appointments": serializer.data
    })



@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def appointments_consultation(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    try:
        appointment = Appointment.objects.get(id=id, doctor=doctor)
    except Appointment.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })
    appointment.status = request.data.get('status')
    appointment.appointment_duration = request.data.get('appointment_duration')
    appointment.save()
    return Response({
        "status_code": 6000,
        "appointments": appointment
    })




@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def appointment_detail(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    try:
        appointment = Appointment.objects.get(id=id, doctor=doctor)
    except Appointment.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })
    serializer = AppointmentSerializer(appointment)
    return Response({
        "status_code": 6000,
        "appointment": serializer.data
    })



@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def appointment_complete(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    try:
        appointment = Appointment.objects.get(id=id, doctor=doctor)
    except Appointment.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Appointment not found"
        })
    appointment.status = 'completed'
    appointment.appointment_duration = request.data.get('appointment_duration')
    appointment.save()
    return Response({
        "status_code": 6000,
        "message": "Appointment completed successfully"
    })























@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescription_single(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointment = Appointment.objects.get(id=id, doctor=doctor)
    try:
        prescription = Prescription.objects.get(appointment=appointment)
    except Prescription.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Prescription not found"
        })
    serializer = PrescriptionSerializer(prescription)
    return Response({
        "status_code": 6000,
        "prescription": serializer.data
    })
 



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescription_list(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointment_complete = Appointment.objects.filter(doctor=doctor, status='completed')
    prescriptions = Prescription.objects.filter(appointment__in=appointment_complete)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response({
        "status_code": 6000,
        "prescriptions": serializer.data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescription_patient(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointment_complete = Appointment.objects.filter(doctor=doctor, status='completed')
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response({
            "status_code": 404,
            "message": "Patient not found"
        })
    prescriptions = Prescription.objects.filter(patient=patient, appointment__in=appointment_complete)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response({
        "status_code": 6000,
        "prescriptions": serializer.data
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescription_create(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointment = Appointment.objects.get(id=id, doctor=doctor)
    patient = appointment.patient

    title = request.data.get('title')
    notes = request.data.get('notes')
    duration = request.data.get('duration')

    prescription = Prescription.objects.create(
        patient=patient,
        appointment=appointment,
        title=title,
        notes=notes,
        duration=duration
    )

    
    return Response({
        "status_code": 6000,
        "message": "Prescription created successfully",
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescription_update(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)

    prescription = Prescription.objects.get(id=id, appointment__doctor=doctor)

    notes = request.data.get('notes')
    duration = request.data.get('duration')

    prescription.notes = notes
    prescription.duration = duration
    prescription.save()

    return Response({
        "status_code": 6000,
        "message": "Prescription updated successfully"
    })



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescriptionitem_create(request, id):
    
    prescription = Prescription.objects.get(id=id)
    medicine = request.data.get('medicine')
    dosage = request.data.get('dosage')
    frequency = request.data.get('frequency')
    instructions = request.data.get('instructions')

    prescription_item = PrescriptionItem.objects.create(
        prescription=prescription,
        medicine=medicine,
        dosage=dosage,
        frequency=frequency,
        instructions=instructions
    )

    return Response({
        "status_code": 6000,
        "message": "Prescription item created successfully"
    })



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def prescriptionitem_update(request, id):

    prescription_item = PrescriptionItem.objects.get(id=id)
    medicine = request.data.get('medicine')
    dosage = request.data.get('dosage')
    frequency = request.data.get('frequency')
    instructions = request.data.get('instructions')

    prescription_item.medicine = medicine
    prescription_item.dosage = dosage
    prescription_item.frequency = frequency
    prescription_item.instructions = instructions
    prescription_item.save()

    return Response({
        "status_code": 6000,
        "message": "Prescription item updated successfully"
    })


















@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def patient_list(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
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
@permission_classes([IsAuthenticated, IsDoctor])
def patient_detail(request, id):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    customer = Customer.objects.get(id=id)
    try:
        patient = Patient.objects.get(customer=customer, appointments__doctor=doctor)
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