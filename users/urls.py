from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from users.apps import UsersConfig
from users.views import UserCreateApiView, UserListApiView, UserRetrieveApiView, UserUpdateApiView, UserDestroyApiView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateApiView.as_view(), name='register_user'),
    path('list/', UserListApiView.as_view(), name='list_user'),
    path('profile/<int:pk>/', UserRetrieveApiView.as_view(), name='profile_user'),
    path('update/<int:pk>/', UserUpdateApiView.as_view(), name='update_user'),
    path('delete/<int:pk>/', UserDestroyApiView.as_view(), name='delete_user'),

    # Jwt token
    path('login/', TokenObtainPairView.as_view(permission_classes=(permissions.AllowAny,)), name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]