"""drones_musala URL Configuration

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from drones import views

router = routers.DefaultRouter()
router.register(r'drones', views.DroneViewSet)
router.register(r'medications', views.MedicationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('accounts/', include('rest_framework.urls')),
]

# Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Drones API",
        default_version='v1.0.0',
        description="API to manage drones and medications to be delivered",
        contact=openapi.Contact(name='Leduan B. Rosell', email="leduanb@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
   re_path(r'^api-docs/swagger/$', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
   re_path(r'^api-docs/redoc/$', schema_view.with_ui('redoc'), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
