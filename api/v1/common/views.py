from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from .serializers import *




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')

    user = authenticate(email=email, password=password)

    if user and user.is_superuser and role == 'admin':
        refresh = RefreshToken.for_user(user)
        data = {
            'access' : str(refresh.access_token),
            'user' : UserSerializer(user, context = {'request' : request}).data
        }

        return Response({'status_code' : 6000, 'data' : data, 'role': 'admin'})

    elif user and user.is_doctor and role == 'doctor':
        refresh = RefreshToken.for_user(user)
        data = {
            'access' : str(refresh.access_token),
            'user' : UserSerializer(user, context = {'request' : request}).data
        }

        return Response({'status_code' : 6000, 'data' : data, 'role': 'doctor'})

    elif user and user.is_hospital_staff and role == 'staff':
        refresh = RefreshToken.for_user(user)
        data = {
            'access' : str(refresh.access_token),
            'user' : UserSerializer(user, context = {'request' : request}).data
        }

        return Response({'status_code' : 6000, 'data' : data, 'role': 'staff'})
    return Response({'status_code' : 6001, 'error' : 'Invalid credentials'})