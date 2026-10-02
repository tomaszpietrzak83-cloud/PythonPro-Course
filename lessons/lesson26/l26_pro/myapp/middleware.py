# TASK 16, 17, 22, 23
import time
import uuid

from django.conf import settings
from django.http import JsonResponse


# TASK 07
class SimpleMethodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(f"Request method:: {request.method}")

        response = self.get_response(request)

        print(f"Status: {response.status_code}")

        return response


# TASK 11
class AddHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        response["X-App-Name"] = "My custom header"

        return response


# TASK 12
class BeforeResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        print("Before response")

        return response


# TASK 12
class AfterResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        print("After response")

        return response


# TASK 16
class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - started_at) * 1000
        response["X-Response-Time"] = f"{duration_ms:.2f} ms"
        print(f"{request.method} {request.path} obsłużono w {duration_ms:.2f} ms")
        return response


# TASK 17
from django.http import JsonResponse


class ClientIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_private_api = request.path.startswith("/api/private/")
        client_id = request.headers.get("X-Client-Id")

        if is_private_api and not client_id:
            return JsonResponse(
                {"detail": "Brak wymaganego nagłówka X-Client-Id."},
                status=403,
            )
        return self.get_response(request)


# TASK 22
class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response


# TASK 23
class BlockIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = request.META.get("REMOTE_ADDR")
        if client_ip in settings.BLOCKED_IPS:
            return JsonResponse(
                {"detail": "Dostęp z tego adresu IP został zablokowany."},
                status=403,
            )
        return self.get_response(request)
