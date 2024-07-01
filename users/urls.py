from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import AuthenticationView, ProfileView, ListProfileView, InvitationView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', AuthenticationView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('profile/invitation/', InvitationView.as_view()),
    path('profiles/', ListProfileView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
