from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True,required=True)

     class Meta:
          model=User
          fields = ['username','email','password']

     def create(self,validated_data):
          user = User.objects.create_user(
               username=validated_data['username'],
               email = validated_data['email'],
               password= validated_data['password']
          )  
          return user

class LoginSerializer(serializers.Serializer):
     username = serializers.CharField()
     password = serializers.CharField(write_only = True)     

# serializer to create profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest the user serializer to include username and email
    
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'profile_picture']

     


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError("New password cannot be the same as the old password")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
