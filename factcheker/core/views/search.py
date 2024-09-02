from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from rest_framework import status

from core.checker import meili_search

@api_view(['GET'])
@login_required
def search_view(request):
    # TODO: Rate limit
    query = request.query_params.get('q')
    if not query:
        return Response({"error": "A query is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    results = meili_search(query, 10)
    results = [result.__dict__() for result in results]

    return Response(results, status=status.HTTP_200_OK)
