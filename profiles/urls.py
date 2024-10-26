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
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/<int:user_id>/', views.ResetPasswordView.as_view(), name='reset_password'),
    
    path('register/', views.RegisterStudentView.as_view(), name='register'),
    path('login/',views.LoginStudentView.as_view(), name='login'),

    path('profile/', views.CurrentUserProfileView.as_view(), name='current-profile'),

    path('', include(router.urls)),
]