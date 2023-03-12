from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from root import settings

urlpatterns = [
    path('api/v1/', include('apps.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Azan Market API",
            default_version='v1',
            description="",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact('GitHub Repository', 'https://github.com/GaniyevUz'),
            license=openapi.License(name='MIT License'),
        ),
        public=True,
        patterns=urlpatterns,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
