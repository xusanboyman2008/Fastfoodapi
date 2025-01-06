from django.http import JsonResponse
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from AUTH_USER.models import ExpiringToken


class ExpiringTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):

        auth_header = get_authorization_header(request)
        if not auth_header:
            return JsonResponse({'error': 'Missing Authorization header.'}, status=401)

        auth_header = auth_header.decode("utf-8").strip()

        token_key = auth_header.split()[1]
        print(token_key)

        try:
            token = ExpiringToken.objects.get(key=token_key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        # Check if the token is expired
        if token.is_expired():
            return JsonResponse({'error': 'Token has expired. Please log in again.'}, status=401)

        # Return the user and token
        return token.user, token
