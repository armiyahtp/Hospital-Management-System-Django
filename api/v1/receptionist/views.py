from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import authenticate
from .serializers import *
from common.serializers import *
from receptionist.models import *





@api_view(['POST'])
@permission_classes([AllowAny])
def receptionist_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user and user.is_receptionist:
        refresh = RefreshToken.for_user(user)
        data = {
            'access' : str(refresh.access_token),
            'user' : UserSerializer(user, context = {'request' : request}).data
        }

        return Response({'status_code' : 6000, 'data' : data})
    return Response({'status_code' : 6001, 'error' : 'Invalid credentials'})




@api_view(['POST'])
@permission_classes([AllowAny])
def receptionist_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            phone_number=serializer.validated_data.get('phone_number'),
            password=serializer.validated_data['password'],
            is_receptionist=True
        )
        Receptionist.objects.create(user=user)
        return Response({"status_code": 6000, "message": "User created successfully"})
    return Response({"status_code": 6001, "error": serializer.errors})