from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog_Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the author     
    title = models.CharField(max_length=255)  # Title of the error post
    description = models.TextField()           # Brief description of the error
    solution = models.TextField()              # Detailed solution to the error
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the post was created
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp of the last update
    programming_language_tags = models.CharField(max_length=100, blank=True)   # Optional tags for categorization

    def __str__(self):
        return self.title