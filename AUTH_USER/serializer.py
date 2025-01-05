from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Permission, Permissions


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()  # Define a custom method for the field

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'permissions']

    def get_permissions(self, obj):
        permissions = Permission.objects.filter(user=obj)  # Get Permission instances for this user
        permission_names = []
        for permission in permissions:
            permission_names.extend([perm.name for perm in permission.permissions.all()])
        return permission_names




class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'
