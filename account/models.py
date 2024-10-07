from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


class User(AbstractUser):
    
    
    activation_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    username = None
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="users")
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    
class Staff(models.Model):
    facebook = models.URLField(null = True)
    twitter = models.URLField(null = True)
    linkedin = models.URLField(null = True)
    position = models.CharField(max_length=30, default="")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.position} - {self.user.first_name}" 
    

class Phone(models.Model):
    phone = models.CharField(max_length=30, default="")
    
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.phone}" 
    
class Address(models.Model):
    street = models.CharField(max_length=30, default="")
    city = models.CharField(max_length=30, default="")
    
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.street} {self.city}" 
    
class Counter(models.Model):
    title = models.CharField(max_length=30, default="")
    number = models.IntegerField()
    
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title}" 
    
class Trustedclient(models.Model):
    image = models.ImageField(upload_to="trusted")
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
class Project(models.Model):
    image = models.ImageField(upload_to="project")
    company = models.CharField(max_length=40, default="")
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    
class Testimonial(models.Model):
   
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    text = models.TextField()
    active = models.BooleanField(default=False)
    datecreated = models.DateTimeField(auto_now_add=True)
    
    
    

