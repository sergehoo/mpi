from django.urls import include, path
from rest_framework.routers import DefaultRouter

from patient.apis.views import PatientViewSet, PlatformViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'platforms', PlatformViewSet)

urlpatterns = [
    path('', include(router.urls)),
]