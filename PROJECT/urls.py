"""PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from core.api.views import account_properties_view, update_user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("core.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("core.api.urls")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")), # Handles other authentication requets such as login and logout
    path("api/v1/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")), # Register a new user
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"), # Schema 
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",), # The documentation
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('api/properties', account_properties_view, name="properties"), # Allows a user to retrieve their details
    path("api/properties/update", update_user_view, name="properties-update"), # Allows a user to update their details

]
