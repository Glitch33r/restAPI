from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/social-network/', include('social_network.urls')),
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),
]
