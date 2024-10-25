from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)  # Profile info like birthdate and hobbies
    birthday = models.DateField(null=True)
    profession = models.CharField(max_length=100,null=True)
    password_requirements = models.CharField(max_length=100,null=True)  # Description of password rules (e.g., must have uppercase, etc.)
    password = models.CharField(max_length=100,null=True)  # Store the actual password
    max_attempts = models.IntegerField(default=1000,null=True)  # Limit on guesses

    def __str__(self):
        return self.name
    