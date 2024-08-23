from rest_framework import serializers
from .models import Blog_Post

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Post
        fields = ['id', 'title', 'description', 'solution', 'created_at', 'updated_at', 'programming_language_tags']
        read_only_fields = ['id', 'created_at', 'updated_at']  # Mark fields as read-only that should not be set by the client