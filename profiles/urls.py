from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register the ProfileViewSet
router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('validate-password/<int:id>/', views.validate_password_guess, name='validate_password_guess'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/<int:user_id>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('register/', views.RegisterStudentView.as_view(), name='register'),
    path('', include(router.urls)),
]