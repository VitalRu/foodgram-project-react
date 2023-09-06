from django.urls import include, path
from rest_framework import routers


app_name = 'api'

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
]
