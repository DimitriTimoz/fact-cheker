from django.contrib import admin
from django.urls import include, path

from core import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('check/', views.fact_check_view),
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('csrf', views.get_csrf_token),
    path('user/', views.get_user_infos),
    path('search/', views.search_view),
]
