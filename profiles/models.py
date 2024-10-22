from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Profile info like birthdate and hobbies
    password = models.CharField(max_length=100)  # Store the actual password
    max_attempts = models.IntegerField(default=1000)  # Limit on guesses

    def __str__(self):
        return self.name