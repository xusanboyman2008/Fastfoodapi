from functools import wraps
from django.http import JsonResponse
import logging
from rest_framework.authentication import get_authorization_header

from AUTH_USER.models import ExpiringToken

logger = logging.getLogger(__name__)


# def check_token(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         auth_header = get_authorization_header(request).decode("utf-8")
#         token_key = auth_header.split()[1]
#         try:
#             token = ExpiringToken.objects.get(key=token_key)
#         except ExpiringToken.DoesNotExist:
#             return JsonResponse({'error': 'Invalid token or token not found.'}, status=401)
#         if token.is_expired():
#             return JsonResponse({'error': 'Token has expired. Please log in again.'}, status=401)
#         return func(request, *args, **kwargs)
#
#     return wrapper


def check_token(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = get_authorization_header(request).decode("utf-8")

        # Check if the Authorization header is properly formatted
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)

        # Extract the token part of the header
        token_key = auth_header.split()[1]

        # Try to get the token from the database
        try:
            token = ExpiringToken.objects.get(key=token_key)
        except ExpiringToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token or token not found.'}, status=401)

        # Check if the token is expired
        if not token.is_expired():
            return JsonResponse({'error': 'Token has expired. Please log in again.'}, status=401)

        # Continue to the original view if token is valid
        return func(request, *args, **kwargs)

    return wrapper