from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .checker import *

@api_view(['POST'])
def fact_check_view(request):
    content = request.data.get('content')
    reviews, conclusion = fact_check(content)
    result = {
        "content": content,
        "reviews": reviews,
        "conclusion": conclusion,
    }
    return Response(result, status=status.HTTP_200_OK)
