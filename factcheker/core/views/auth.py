from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# TODO: Add error handling
@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if the email is already used
    if User.objects.filter(email=email).exists():
        return Response({
            "error": "Email already used."
            }, status=status.HTTP_409_CONFLICT)
    
    # Check if the email is valid   
    if not email or not "@" in email:
        return Response({
            "error": "Invalid email."
            }, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=email, password=password, email=email)
    user.save()
    
    # Login the user
    django_request = request._request
    login(django_request, user)
    
    return Response(status=status.HTTP_201_CREATED)

# TODO: Add error handling
@csrf_exempt
@api_view(['POST'])
def login_view(request: Request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Use Django's HttpRequest for authentication and login
    django_request = request._request
    user = authenticate(request=django_request, username=email, password=password)
    
    if user is None:
        return Response({
                "error": "Invalid credentials."
            }, status=status.HTTP_404_NOT_FOUND)
    
    login(django_request, user)
    return Response(
        status=status.HTTP_200_OK)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
