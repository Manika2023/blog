from django.contrib import admin
from .models import Blog_Post
# Register your models here.
@admin.register(Blog_Post)
class BlogAdmin(admin.ModelAdmin):
     list_display=['id','author','title','description','solution','created_at','updated_at','programming_language_tags']

