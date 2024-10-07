from django.contrib.auth.backends import ModelBackend
from .models import User

class AuthBackend(ModelBackend):

    def authenticate(self, request, identity=None, password=None):
        try:
            user = User.objects.get(email = identity)
            
            if user.check_password(password) and user.is_active == True:
                return user
            
            elif user.check_password(password) and user.is_active == False:
                return NameError("inactive")
        except User.DoesNotExist:
            return None
