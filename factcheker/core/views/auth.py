from django.contrib.auth.models import User


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
