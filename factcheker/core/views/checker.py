
from django.contrib.auth.decorators import login_required
from datetime import date

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.checker import fact_check
from core.models import UserProfile

@api_view(['POST'])
@login_required
def fact_check_view(request):
    # TODO: Error handling
    content = request.data.get('content')
    
    # Check rate limit
    user = request.user
    profile = UserProfile.objects.get(user=user)
    
    if profile.last_used.day != date.today().day:
        profile.usage = 0
    if profile.usage >= profile.rate_limit:
        return Response({"error": "Rate limit exceeded, try tomorrow"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    profile.usage += 1
    profile.save()
    reviews, conclusion = fact_check(content)
    result = {
        "content": content,
        "reviews": reviews,
        "conclusion": conclusion,
    }
    
    return Response(result, status=status.HTTP_200_OK)
