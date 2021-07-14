
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import message, send_mail
import uuid

from django.conf import settings

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 , null=True,blank=True)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

