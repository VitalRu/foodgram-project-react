from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="v1talrudenko@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path(r'^swagger(?P<format>\.json|\.yaml)$',
    #      schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
    #      name='schema-swagger-ui'),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
