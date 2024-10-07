from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, text = None, password = None ):  
        userModel = get_user_model()

        try:
            user  = userModel.objects.get(email = text) or userModel.objects.get(username = text)
        except userModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user