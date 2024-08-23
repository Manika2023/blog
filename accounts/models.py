from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
     user=models.OneToOneField(User,on_delete=models.CASCADE)
     bio=models.TextField(blank=True)
     location = models.CharField(max_length=100,blank=True)
     profile_picture=models.ImageField(upload_to='profile_pics/',blank=True)

     def __str__(self):
          return f'{self.user.username} Profile'

# use fo signal in modals.py
# signal when user will register , it will automaticcally create profile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
     if created:
          Profile.objects.create(user=instance)
          

@receiver(post_save,sender=User)          
def save_user_profile(sender,instance,**kwargs):
     instance.profile.save()