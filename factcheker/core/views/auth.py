from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if the email is already used
    if User.objects.filter(email=email).exists():
        return Response(status=status.HTTP_409_CONFLICT)
    
    # Check if the email is valid   
    if not email or not "@" in email:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=email, password=password, email=email)
    user.save()
    print(user.username, "registered")
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt # TODO: Remove this line
def login_view(request: Request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Use Django's HttpRequest for authentication and login
    django_request = request._request
    user = authenticate(request=django_request, username=email, password=password)
    
    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    login(django_request, user)
    
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
