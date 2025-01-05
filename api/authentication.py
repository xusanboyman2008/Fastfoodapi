from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from AUTH_USER.models import ExpiringToken


class ExpiringTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Log all headers for debugging
        print("Headers:", request.headers)

        # Extract the Authorization header
        auth_header = get_authorization_header(request).decode('utf-8')
        print("Authorization Header:", auth_header)  # Debugging

        if not auth_header or not auth_header.startswith('Token '):
            return None

        # Extract the token key
        token_key = auth_header.split()[1]

        try:
            token = ExpiringToken.objects.get(key=token_key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        # Check if the token is expired
        if token.is_expired():
            raise AuthenticationFailed('Token has expired. Please log in again.')

        # Return the user and token
        return token.user, token
