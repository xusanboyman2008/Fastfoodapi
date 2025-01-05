from django.contrib import admin

from AUTH_USER.models import Permission, Permissions

admin.site.register(Permission)
admin.site.register(Permissions)