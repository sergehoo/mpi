from django.http import JsonResponse

from patient.models import Platform


class PlatformAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        platform_name = request.headers.get('Platform-Name')
        if platform_name:
            try:
                platform = Platform.objects.get(name=platform_name)
                if not platform.is_active:
                    return JsonResponse({"error": "Accès refusé : plateforme désactivée"}, status=403)
            except Platform.DoesNotExist:
                return JsonResponse({"error": "Plateforme non reconnue"}, status=403)
        return self.get_response(request)