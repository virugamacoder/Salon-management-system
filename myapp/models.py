from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,PermissionsMixin  
from django.db import models
from .manager import UserManager
import os

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)

# ALTER TABLE myapp_user DROP INDEX username
class User(AbstractUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    phone = models.CharField(max_length=20,default='')
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True) 
    
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True) 
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'
        
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='') 
    uimg = models.ImageField(upload_to="user/images",default="") 
     
    def __str__(self):
        return self.email
    
    def delete(self, *args, **kwargs):
        # delete the file from the file system
        if self.uimg:
            os.remove(self.uimg.path)

        # call the parent class delete method to delete the object
        super(User, self).delete(*args, **kwargs)

class OTP(models.Model):
    email = models.EmailField(max_length=254,default=" ")
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)   
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


# class Customer1(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)

       
class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    contactno = models.CharField(max_length=10)
    
    def __str__(self):  
        return self.aname
    
    
