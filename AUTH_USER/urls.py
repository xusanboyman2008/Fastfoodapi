from django.urls import path
from .views import login, logout, create_user, add_permission, get_user, delete_user, create_permission, \
    update_permission

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('create_user/', create_user, name='create_user'),
    path('add_permissions/<user_id>/', add_permission, name='add-permissions-to-user'),
    path('user/<user_id>/', get_user , name='get-user'),
    path('delelte/<user_id>/',delete_user),
    path('create_permission/',create_permission),
    path('update_permission/<permission_id>/',update_permission)

]
