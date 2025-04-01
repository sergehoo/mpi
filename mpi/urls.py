from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from patient.apis.views import PlatformTokenView
from patient.views import Landing

urlpatterns = [
                  path('ac/mpi/ogah/', admin.site.urls),
                  path('apis-auth/', include('rest_framework.urls')),
                  path('mpi/', include('patient.apis.urls')),

                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('platform/token/', PlatformTokenView.as_view(), name='platform_token'),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('', Landing.as_view(), name='landing'),
                  path('contact/', contact_view, name='contact'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
