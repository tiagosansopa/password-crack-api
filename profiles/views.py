import json
import exrex
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Attempt  # Import Attempt model
from django.utils import timezone  # Import timezone for timestamping
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from .serializers import ProfileSerializer, UserProfileSerializer
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.http import JsonResponse
from .models import Profile, Attempt
import json
import exrex

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_password_guess(request, id):
    profile = Profile.objects.get(id=id)
    user = request.user

    body = request.data
    guess_pattern = body.get('pattern')
    max_attempts = int(body.get('max_attempts', 100000))

    success, attempts = try_crack_password(profile.password, guess_pattern, max_attempts)
    Attempt.objects.create(
        profile=profile,
        user=user,
        regex_used=guess_pattern,
        successful=success,
        timestamp=timezone.now()
    )

    if success:
        profile.cracked = True
        profile.save()

    if success:
        return JsonResponse({"success": True, "message": f"Password encontrado en {attempts} intentos.", "password": f"{profile.password}"})
    else:
        return JsonResponse({"success": False, "message": f"Password no encontrado en {attempts} intentos."})


def try_crack_password(actual_password, pattern, max_attempts):
    attempts = 0
    used_guesses = set()
    while attempts < max_attempts:
        guess = exrex.getone(pattern)
        used_guesses.add(guess)
        attempts += 1
        if guess == actual_password:
            return True, attempts
    return False, attempts

class RegisterStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get("fullName")
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        first_name, *last_name = full_name.split(" ", 1)
        last_name = last_name[0] if last_name else ""

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "fullName": f"{user.first_name} {user.last_name}"
            }
        })

class LoginStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user.username
            })
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordView(APIView):
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        new_password = request.data.get("new_password")
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."})

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        profile_data = serializer.data
        profile_data['attempt_count'] = profile.attempts.count()
        return Response(profile_data)

class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
