from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)  # Profile info like birthdate and hobbies
    birthday = models.DateField(null=True)
    profession = models.CharField(max_length=100, null=True)
    password_requirements = models.CharField(max_length=100, null=True)  # Description of password rules
    password = models.CharField(max_length=100, null=True)  # Store the actual password
    max_attempts = models.IntegerField(default=1000, null=True)  # Limit on guesses
    cracked = models.BooleanField(default=False)  # Indicates if the password was cracked

    def __str__(self):
        return self.name

class Attempt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the attempt
    regex_used = models.CharField(max_length=200)  # The regex used in the attempt
    successful = models.BooleanField(default=False)  # Whether the attempt was successful
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the attempt

    def __str__(self):
        return f"Attempt by {self.user} on {self.profile.name} - Success: {self.successful}"