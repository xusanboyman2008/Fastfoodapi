from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from .models import ExpiringToken, User, Permission, Permissions
from .serializer import UserSerializer, PermissionsSerializer
import json


@csrf_exempt
def login(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")
                role = data.get("role")
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Handle form data
        elif request.content_type == "application/x-www-form-urlencoded":
            username = request.POST.get("username")
            password = request.POST.get("password")
            role = request.POST.get("role")

        # Unsupported content type
        else:
            return JsonResponse({'error': 'Unsupported Content-Type'}, status=415)

        # Validate inputs
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)

        # Authenticate user
        if not role:
            user = authenticate(request, username=username, password=password)
        else:
            if role not in ['admin', 'manager','user']:
                return JsonResponse({'error': 'Invalid role', 'data': role}, status=400)
            user = authenticate(request, username=username, password=password, role=role)

        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        # Get or create the user's token
        token, created = ExpiringToken.objects.get_or_create(user=user)

        # If the token exists but has expired, delete it and create a new one
        if not created and token.is_expired():
            token.delete()
            token = ExpiringToken.objects.create(user=user)

        user_data = UserSerializer(user).data
        response = JsonResponse(
            {'message': 'Login successful', 'expires_at': token.expires_at.isoformat(), 'token': token.key,
             'user': user_data}
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
        role = request.POST.get("role")
        # Validate username and password
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)
        if role:
            if role not in ['admin', 'manager']:
                return JsonResponse({'error': 'Invalid role', 'data': role}, status=400)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Create new user
        if role in ['admin', 'manager']:
            user = User.objects.create_user(username=username, password=password, email=username, role=role)
        else:
            user = User.objects.create_user(username=username, password=password, email=username)
        return JsonResponse({'message': 'User created successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
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


@csrf_exempt
def add_permission(request, user_id):
    predefined_permissions = ['Can view', 'Can edit', 'Can delete']
    for perm_name in predefined_permissions:
        if not Permissions.objects.filter(name=perm_name).exists():
            Permissions.objects.create(name=perm_name)

    if request.method == "POST":
        permission_id = request.POST.get("permission")
        if not permission_id:
            return JsonResponse({'error': 'Permission ID is required'}, status=400)
        if not permission_id.isdigit():
            return JsonResponse({'error': 'Invalid permission ID, must be a number'}, status=400)
        permission_id = int(permission_id)

        try:
            user_role = User.objects.get(id=user_id)  # Use user_id directly here
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user_role.role == 'Usesr':  # Fixed typo here
            return JsonResponse({'error': 'User cannot add permissions'}, status=400)

        try:
            permission_instance = Permissions.objects.get(id=permission_id)
        except Permissions.DoesNotExist:
            return JsonResponse({'error': 'Permission with this ID does not exist'}, status=400)

        # Get or create the permission instance for the user
        permission, created = Permission.objects.get_or_create(user=user_role)
        permission.permissions.add(permission_instance)

        user_role_s = UserSerializer(user_role).data

        return JsonResponse({'message': 'Permission added successfully', 'user': user_role_s}, status=201)


@csrf_exempt
def get_user(request, user_id):
    if request.method == "POST":
        user_role = User.objects.get(id=user_id)
        user = UserSerializer(user_role).data
        return JsonResponse({'user': user})
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})


@csrf_exempt
def create_permission(request):
    if request.method == "POST":
        permission_name = request.POST.get("name")
        if not permission_name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        # Check if the permission already exists
        permission, created = Permissions.objects.get_or_create(name=permission_name)

        if created:
            return JsonResponse({'message': 'Permission created successfully'}, status=201)
        else:
            return JsonResponse({'message': 'Permission already exists'}, status=200)

    elif request.method == "GET":
        permissions = Permissions.objects.all()

        # Serialize the permissions
        serializer = PermissionsSerializer(permissions, many=True)

        return JsonResponse({'permissions': serializer.data}, status=200)


@csrf_exempt
def update_permission(request, permission_id):
    if request.method == "POST":
        try:
            permission_name = request.POST.get("name")
            if not permission_name:
                return JsonResponse({'error': 'Permission name is required'}, status=400)

            permission = Permissions.objects.get(id=permission_id)
            permission.name = permission_name  # Update the permission name
            permission.save()  # Save the changes

            return JsonResponse({'message': 'Permission updated successfully'}, status=200)

        except Permission.DoesNotExist:
            return JsonResponse({'error': 'Permission not found'}, status=404)


    elif request.method == "DELETE":
        try:
            permission = Permissions.objects.get(id=permission_id)
            permission.delete()  # Delete the permission
            return JsonResponse({'message': 'Permission deleted successfully'}, status=200)

        except Permission.DoesNotExist:
            return JsonResponse({'error': 'Permission not found'}, status=404)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
