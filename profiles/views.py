import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json


def check_connection(request):
    return Response({"message": "Django API is connected"})

@csrf_exempt
def get_profile(request, id):
    profile = Profile.objects.get(id=id)
    data = {
        "name": profile.name,
        "description": profile.description,
        "max_attempts": profile.max_attempts
    }
    return JsonResponse(data)

@csrf_exempt
def validate_password(request, id):
    profile = Profile.objects.get(id=id)
    body = json.loads(request.body)
    guessed_password = body.get("password")

    if guessed_password == profile.password:
        return JsonResponse({"success": True, "message": "Password cracked!"})
    else:
        return JsonResponse({"success": False, "message": "Incorrect password."})


@csrf_exempt
def test_script(request, id):
    # Get the profile for which the password needs to be cracked
    profile = Profile.objects.get(id=id)
    script = request.FILES['script']

    # Save the uploaded Python script temporarily
    with open('uploaded_script.py', 'wb') as f:
        f.write(script.read())

    # Execute the script in a sandboxed environment
    try:
        result = subprocess.run(
            ['python3', 'uploaded_script.py'],  # Call the uploaded script
            capture_output=True,                # Capture stdout and stderr
            text=True,                          # Decode output as text
            timeout=5                           # Limit execution time to 5 seconds
        )

        # Check if the student's script successfully guessed the password
        if profile.password in result.stdout:
            message = "Password cracked!"
        else:
            message = "Incorrect password or not found in script output."

    except subprocess.TimeoutExpired:
        message = "Script execution timed out."
    except subprocess.CalledProcessError as e:
        # Capture any errors from the script execution
        message = f"Script failed with error: {e}"

    # Clean up the temporary file (optional)
    # os.remove('uploaded_script.py')

    return JsonResponse({"message": message})