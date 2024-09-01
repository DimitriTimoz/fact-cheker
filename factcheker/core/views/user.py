from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from core.models import UserProfile
from datetime import date, timedelta

@api_view(['GET'])
@login_required
def get_rate_limit(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if profile.last_used.day != date.today().day:
        profile.usage = 0
        profile.save()
    
    next_resest = profile.last_used + timedelta(days=1)
    # Set to midnight
    next_resest = next_resest.replace(hour=0, minute=0, second=0, microsecond=0)
    
    return Response({
        "limit": profile.rate_limit,
        "usage": profile.usage,
        "next_reset": next_resest
    })
