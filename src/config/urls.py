from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/companies", include("apps.companies.urls")),

    
    
    # 1. Direct path to download the schema (YAML by default)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI: Interactive documentation
    # url_name='schema' tells it where to fetch the OpenAPI definition
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc: Clean, static documentation
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Include your app URLs here
    # path('api/accounts/', include('apps.accounts.urls')),
]    