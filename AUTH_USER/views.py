from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.utils import json

from decorator import check_token
from .models import ExpiringToken, User


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate input
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        # Get or create the user's token
        token, created = ExpiringToken.objects.get_or_create(user=user)

        # If the token exists but has expired, delete it and create a new one
        if not created and token.is_expired():
            token.delete()
            token = ExpiringToken.objects.create(user=user)

        # Return the token in the response header
        response = JsonResponse(
            {'message': 'Login successful', 'expires_at': token.expires_at.isoformat(), 'token': token.key}
        )

        # Set the Authorization header in the response
        response['Authorization'] = f'Token {token.key}'

        return response

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)
        if username not in User.objects.all():
            user = User.objects.create_user(username=username, password=password)
        else:
            return JsonResponse({'error': 'Username already exists'}, status=400)

@csrf_exempt  # Optional, depending on your CSRF setup for API views
def logout(request):
    # Get the token from the Authorization header
    auth_header = get_authorization_header(request).decode("utf-8")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)

    token_key = auth_header.split()[1]

    try:
        # Try to find the ExpiringToken object
        token = ExpiringToken.objects.get(key=token_key)

        # Delete the token to log the user out
        token.delete()

        return JsonResponse({'message': 'Logged out successfully'})
    except ExpiringToken.DoesNotExist:
        # If the token does not exist, return an error message
        return JsonResponse({'error': 'Invalid token or token not found.'}, status=401)
