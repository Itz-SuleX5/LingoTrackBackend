from django.urls import path
from .views import (
    create_or_update_user,
    get_user_profile,
    get_all_users,
    delete_all_users
)

urlpatterns = [
    path('', create_or_update_user),
    path('profile/', get_user_profile),
    path('all/', get_all_users),
    path('delete-all/', delete_all_users),
]
