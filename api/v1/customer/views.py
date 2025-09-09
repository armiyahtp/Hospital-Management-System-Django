from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import authenticate
from .serializers import *
from api.v1.common.serializers import UserSerializer
from customer.models import *





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