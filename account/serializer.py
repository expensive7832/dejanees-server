from rest_framework import serializers

from .models import  User, Staff
 
from django.contrib.auth import authenticate
from rest_framework.exceptions import bad_request
import string
from random import choice
# import json   
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os

class UserSerializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    photo = serializers.ImageField()
    # activation_code = serializers.CharField(default="")
    
    class Meta:
        model = User
        fields = ['is_active', 'is_superuser', 'first_name', "photo", 'last_name', 'email', 'password']
        
    def validate(self, attrs):
        
        try:
            user = User.objects.filter(email = attrs['email']).first()
        
            if user is not None:
                raise serializers.ValidationError("user already exists")
            return super().validate(attrs)
        except BaseException as e:
            raise serializers.ValidationError({"error": str(e)}, 400)
    
    def create(self, data):
        
        
        
        
        chars = string.digits
            
        random =  ''.join(choice(chars) for _ in range(4))
        
        user = User.objects.create_user(
            email = data['email'],
            first_name = data['email'],
            last_name = data['last_name'],
            password = data['password'],
            activation_code = random
        )
        
       
        
       
        
        
        return data


class StaffSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only = True)
    user = UserSerializer(read_only = True)
    position = serializers.CharField()
    facebook = serializers.URLField()
    linkedin = serializers.URLField()
    twitter = serializers.URLField()
    uid = serializers.IntegerField(write_only = True)
    first_name = serializers.CharField(write_only = True)
    last_name = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    photo = serializers.ImageField(write_only = True)

    
    class Meta:
        model = User
        fields = ['created_by', 'id', 'user', 'photo', 'first_name', 'last_name', 'email', 'position', 'facebook', 'linkedin', 'twitter', 'uid']
        
    def validate(self, attrs):
        
        try:
            user = User.objects.filter(email = attrs['email']).first()
        
            if user is not None:
                raise serializers.ValidationError("user already exists")
            return super().validate(attrs)
        except BaseException as e:
            raise serializers.ValidationError({"error": str(e)}, 400)
    
    def create(self, data):
        
        created_by = User.objects.get(id = data['uid'])
        
        chars = string.digits
            
        random =  ''.join(choice(chars) for _ in range(4))
        
        user = User.objects.create_user(
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            password = "ouhjouy7t68t7",
            photo = data['photo'],
            activation_code = random
        )
        
        newstaff = Staff.objects.create(
            user = user,
            created_by = created_by,
            position = data['position'],
            facebook = data['facebook'],
            linkedin = data['linkedin'],
            twitter = data['twitter']
        )
        
        
        return data

                
        
class LoginSerializer(serializers.Serializer):
    identity = serializers.CharField()
    password = serializers.CharField()
    
   
        

class UpdateUserSerializer(serializers.ModelSerializer):
   
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = serializers.CharField()
    email = serializers.EmailField()
    facebook = serializers.URLField()
    linkedin = serializers.URLField()
    twitter = serializers.URLField()
    image = serializers.ImageField(allow_null = True, required = False)
    oldimage = serializers.CharField()
    
    class Meta:
        model = Staff
        fields = ['first_name','last_name','oldimage', 'image', 'position', 'email', 'facebook', 'linkedin', 'twitter']
        
    def update(self, instance, data):
        
        
        staff = Staff.objects.get(id = instance.id)
        
        user = User.objects.get(id = staff.user.id)
        
        if data['image'] is not None:
            os.remove(f"media/{data['oldimage']}")
      
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.photo = data['image']
        
        staff.position = data['position']
        staff.linkedin = data['linkedin']
        staff.facebook = data['facebook']
        staff.twitter = data['twitter']
        
        
        staff.save()
        user.save()
        
    
        
        return data
        

