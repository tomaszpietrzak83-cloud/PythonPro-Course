from rest_framework.authentication import SessionAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class LocalSessionAuthentication(SessionAuthentication):
    """Także anonimowe zmiany lokalnych danych wymagają tokenu CSRF."""

    def authenticate(self, request):
        self.enforce_csrf(request)
        return super().authenticate(request)


class LocalSessionScheme(OpenApiAuthenticationExtension):
    target_class = "laboratory.authentication.LocalSessionAuthentication"
    name = "cookieAuth"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "cookie", "name": "sessionid"}
