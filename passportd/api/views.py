from django.http import JsonResponse
from django.views.generic import View


class PingView(View):
    def get(self, request):
        return JsonResponse({"status": "OK"})
