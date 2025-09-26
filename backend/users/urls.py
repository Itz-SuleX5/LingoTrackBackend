from django.urls import path
from .views import create_or_update_user, get_user_profile, get_all_users, delete_all_users

urlpatterns = [
    path('', create_or_update_user, name='user-list-create'),
    path('profile/', get_user_profile, name='user-profile'),
    path('all/',get_all_users, name='user-list'),
    path('all/delete', delete_all_users, name='user-list-delete'),
]
