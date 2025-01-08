from django.http import JsonResponse
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from AUTH_USER.models import ExpiringToken


class ExpiringTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        if not auth_header:
            raise AuthenticationFailed('Missing Authorization header.')

        auth_header = auth_header.decode("utf-8").strip()

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed('Invalid authorization header format.')

        token_key = auth_header.split()[1]

        try:
            token = ExpiringToken.objects.get(key=token_key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        # Check if the token is expired
        if token.is_expired():
            raise AuthenticationFailed('Token has expired. Please log in again.')

        # Return the user and token
        return (token.user, token)
