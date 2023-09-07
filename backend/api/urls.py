from django.urls import include, path
from rest_framework import routers


app_name = 'api'

router = routers.SimpleRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
]
