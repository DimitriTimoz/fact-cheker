from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.checker import fact_check

@api_view(['POST'])
@login_required
def fact_check_view(request):
    print(request)
    content = request.data.get('content')
    reviews, conclusion = fact_check(content)
    result = {
        "content": content,
        "reviews": reviews,
        "conclusion": conclusion,
    }
    return Response(result, status=status.HTTP_200_OK)
