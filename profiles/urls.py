from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:id>/', views.get_profile, name='get_profile'),
    path('validate/<int:id>/', views.validate_password, name='validate_password'),
    path('test-script/<int:id>/', views.test_script, name='test_script'),
]