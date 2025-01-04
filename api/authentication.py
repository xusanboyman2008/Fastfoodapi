from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from AUTH_USER.models import ExpiringToken

class ExpiringTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract token from the Authorization header
        auth_header = get_authorization_header(request).decode("utf-8")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed('Authentication credentials were not provided.')

        token_key = auth_header.split()[1]

        # Try to get the token from the database
        try:
            token = ExpiringToken.objects.get(key=token_key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token or token not found.')

        # Check if the token has expired
        if token.is_expired():
            raise AuthenticationFailed('Token has expired. Please log in again.')

        # If token is valid, return the user and token
        return token.user, token  # Here, you can return the associated user if needed
