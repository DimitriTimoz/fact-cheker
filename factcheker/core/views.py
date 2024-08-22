from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .checker import *

@api_view(['POST'])
def fact_check_view(request):
    content = request.data.get('content')
    return Response(generate_key_words(content), status=status.HTTP_200_OK)
