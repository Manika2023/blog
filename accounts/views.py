from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import RegistrationSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,UserSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    # Extract username and email from the request data
    username = request.data.get('username')
    email = request.data.get('email')

    if User.objects.filter(email=email).exists():
        return Response({
            'message': 'You are already registered with this email, please login.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
     # Check if the username or email is already registered
    if User.objects.filter(username=username).exists():
        return Response({
            'message': 'Username or password is already exist, please choose another one.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Proceed with registration if the username and email are not already registered
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        # Django login function to log the user in
        login(request, user)
        return Response({
            'message': "Your registration, login, and profile creation were successful.",
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successfully',
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Invalid credentials, please sign up if you have not'
            }, status=status.HTTP_401_UNAUTHORIZED)  # Use 401 for unauthorized access
    else:
        return Response({
            "message": "Your data is incorrect"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        profile = request.user.profile  # Assuming a OneToOne relationship with User
    except profile.DoesNotExist:
        return Response({'error': "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data.copy()  # Make a mutable copy of request data

        # If there's a file in the request, update profile_picture separately
        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']

        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception or handle it as needed
            return Response({"error": "An unexpected error occurred. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
      try:
           request.user.auth_token.delete()
           return Response({"message":"Successfully logged out"},status=status.HTTP_200_OK)
      except (AttributeError,Token.DoesNotExist):
            return Response({'error':"Token not found or already deleted"},status=status.HTTP_400_BAD_REQUEST) 