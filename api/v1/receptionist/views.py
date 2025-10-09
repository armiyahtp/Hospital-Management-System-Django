from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from django.shortcuts import render
from datetime import datetime, date, timedelta




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
                license_number=license_number
            )
            return Response({"status_code": 6000, "message": "User created successfully"})
        
    return Response({"status_code": 6001, "error": serializer.errors})









@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def create_doctor_availability(request):
    serializer = DoctorAvailabilitySerializer(data = request.data)
    if serializer.is_valid():
        availability = serializer.save()


        return Response({
            "status_code": 6000,
            "message": "Availability created successfully",
            "doctoravailability": serializer.data,
            "availability": availability
        })

    return Response({"status_code": 6001, "error": serializer.errors})




@api_view(['POST'])
@permission_classes([IsAuthenticated, IsReceptionist])
def generate_token(request):
    availability = request.data.get('availability')
    today = date.today()

    Token.objects.filter(appointment_date__lt=today).delete()

    end_date = today + timedelta(weeks=1)
    created_tokens = []

    current_date = today + timedelta(days=1)
    while current_date <= end_date:
        if current_date.weekday() == availability.weekday:
            start_time = availability.start_time
            end_time = availability.end_time
            duration = availability.consult_duration
            tkn = 1


            break_start = (
                datetime.combine(date.today(), availability.break_start)
                if availability.break_start else None
            )

            break_end = (
                datetime.combine(date.today(), availability.break_end)
                if availability.break_end else None
            )

            while start_time < end_time:
                if break_start and break_end:
                    current_start = datetime.combine(date.today(), start_time)
                    if break_start <= current_start < break_end:
                        start_time = break_end.time()
                        continue

                formatted = f'TKN0{tkn}'
                token, created = Token.objects.get_or_create(
                    doctor=availability.doctor,
                    departemnt=availability.doctor.department, 
                    appointment_date=current_date,
                    token_number=formatted,
                    defaults={
                        "start_time": start_time,
                        "end_time": (
                            (datetime.combine(date.today(), start_time) + timedelta(minutes=duration)).time()
                        ),
                        "is_booked": False,
                        "is_canceled": False,
                    }
                )
                if created:
                    created_tokens.append(token.id)
                start_time = (
                    datetime.combine(date.today(), start_time) + timedelta(minutes=duration)
                ).time()
                tkn += 1
        current_date += timedelta(days=1)
    return created_tokens


        