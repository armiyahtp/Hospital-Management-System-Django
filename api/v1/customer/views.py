from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import authenticate
from .serializers import *
from api.v1.common.serializers import UserSerializer
from customer.models import *
from hospital.models import *





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
        Customer.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({"status_code": 6000, 'access' : str(refresh.access_token), "message": "User created successfully"})
    return Response({"status_code": 6001, "error": serializer.errors})





















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

    context = {
        'request' : request
    }

    serializers = DoctorSerializer(instances, many=True, context=context)

    return Response({'status_code':6000, 'data':serializers.data, 'message':'doctor listed'})







@api_view(['GET'])
@permission_classes([AllowAny])
def testimonials(request):
    instances = Testimonial.objects.all()

    context = {
        'request' : request
    }

    serializers = TestimonialSerializer(instances, many=True, context=context)

    return Response({'status_code':6000, 'data':serializers.data, 'message':'testimonial listed'})








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_department(request, id):
    instance = Department.objects.get(id=id)
    doctors = Doctor.objects.filter(department=instance)
    



    context = {
        "request":request
    }

    serializer = DepartmentSerializer(instance, context=context)

    return Response({
        'status_code':6000,
        'department' : serializer.data,
        'doctors' : doctors,
    })











@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_doctor(request, id):
    instance = Doctor.objects.get(id=id)

    context = {
        'request' : request
    }

    serializer = DoctorSerializer(instance, context=context)


    return Response({
        'status_code' : 6000,
        'data' : serializer.data,
    })









@api_view(['POST'])
@permission_classes([IsAuthenticated])
def take_appointment(request, id):
    user = request.user
    

    token = Token.objects.get(id=id)


    patient = Patient.objects.create(
        first_name=user.first_name,
        last_name=user.last_name,
        age=request.data.get("age", 0),
        gender=request.data.get("gender", "Other"),
        phone_number=user.phone_number,
        place=request.data.get("place", "")
    )



    appointment = Appointment.objects.create(
        patient=patient,
        doctor=token.doctor,
        department=token.departemnt,
        token_number=token,
        appointment_date=token.appointment_date,
        start_time=token.start_time,
        end_time=token.end_time,
        status=request.data.get("status", "pending"),
        reason=request.data.get("reason", ""),
        notes=request.data.get("notes", ""),
    )


    token.is_booked = True
    token.save()

    return Response({
        "status_code": 6000,
        "message": "Appointment booked successfully",
        "appointment": appointment,
        "patient": patient,
        "token": token
    })











@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_appointments(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    

    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-start_time')

    result = []
    for appt in appointments:
        result.append({
            "appointment_id": appt.id,
            "doctor": {
                "id": appt.doctor.id,
                "email": appt.doctor.user.email,
            },
            "department": {
                "id": appt.department.id,
                "name": appt.department.name,
            },
            "token": {
                "id": appt.token_number.id,
                "token_number": appt.token_number.token_number,
                "appointment_date": appt.token_number.appointment_date,
                "start_time": appt.token_number.start_time,
                "end_time": appt.token_number.end_time,
                "is_booked": appt.token_number.is_booked,
            },
            "appointment_date": appt.appointment_date,
            "start_time": appt.start_time,
            "end_time": appt.end_time,
            "status": appt.status,
            "reason": appt.reason,
            "notes": appt.notes
        })

    return Response(result)








