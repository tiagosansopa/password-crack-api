import exrex
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

@csrf_exempt
def validate_password_guess(request, id):
    profile = Profile.objects.get(id=id)
    if request.content_type == 'application/json':
        body = json.loads(request.body)
    else:
        body = request.POST
    guess_pattern = body.get('pattern')
    max_attempts = int(body.get('max_attempts', 1000))
    success, attempts = try_crack_password(profile.password, guess_pattern, max_attempts)
    if success:
        return JsonResponse({"success": True, "message": f"Password cracked in {attempts} attempts!"})
    else:
        return JsonResponse({"success": False, "message": f"Failed to crack the password within {attempts} attempts."})


def try_crack_password(actual_password, pattern, max_attempts):
    attempts = 0
    used_guesses = set()

    while attempts < max_attempts:
        guess = exrex.getone(pattern)
        if guess not in used_guesses:
            attempts += 1
            used_guesses.add(guess)
            if guess == actual_password:
                return True, attempts

    return False, attempts
class RegisterStudentView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            password=make_password(password), 
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user.username
        })
    
class ResetPasswordView(APIView):
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        new_password = request.data.get("new_password")
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."})