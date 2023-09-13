from django.db import models
import uuid
# import os
from django.db import models
from django.utils import timezone 
import random

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# custom user manager

#######################################


# class Otp(models.Model):
#     phone_number = models.CharField(max_length=15)
#     otp_code = models.CharField(max_length=6)
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.phone_number} - {self.otp_code}"

###########################################
class MyUserManager(BaseUserManager):
    def create_user(self, email,password):
        """
        Creates and saves a User with the given email, otp and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class VendorRegistration(models.Model):
#     # Custom user model for Vendor Registration
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     Is_Approved = models.BooleanField(default=False)

#     # Additional fields for vendor registration (add more as needed)
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)

#     def __str__(self):
#         return self.email

# class OTP(models.Model):
#     # Model to store OTPs for vendor registration
#     user = models.ForeignKey(VendorRegistration, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.otp}"




# custom user model
class vendorregistration(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField('email',max_length=255,unique=True)
    password = models.CharField(max_length=20, blank=False, null=False)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved= models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Create your models here.

# class vendorregistration(models.Model):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=20, blank=False, null=False)
#     otp = models.CharField(max_length=8, null=True, blank=True)
#     uid = models.UUIDField(default=uuid.uuid4)
#     Otpcreated_at = models.DateTimeField(null=True, blank=True)
#     Is_Approved= models.BooleanField(default=False)
#     is_verified =models.BooleanField(default=False)


class VendorProfile(models.Model):
    vendor = models.ForeignKey(vendorregistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/',null = True,blank =True)
    age = models.IntegerField()
    city = models.CharField(max_length=255)
    working_or_studying = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


@property
def imageURL(self):
    try:
        url = self.profile_picture.url
    except:
        url = ''
    return url

class VendorArtwork(models.Model):
    vendor = models.ForeignKey(vendorregistration, on_delete=models.CASCADE)
    Art_image = models.ImageField(upload_to='images/',null = True, blank =True)
    themes = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    medium = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

@property
def imageURL(self):
    try:
        url = self.Art_image.url
    except:
        url = ''
    return url

class customer(models.Model):
    panting = models.ForeignKey(VendorArtwork, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.BigIntegerField()
    Address = models.CharField(max_length=500)

      



def __str__(self):
    return f"Artwork by {self.vendor.name}"



def __str__(self):
        return self.name



@property
def imageURL(self):
    try:
        url = self.profile_picture.url
    except:
        url = ''
    return url


###################################################

# class CustomerRegistration(models.Model):  
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=20, blank=False, null=False)
#     name = models.CharField(max_length=8, blank=False)
#     uid = models.UUIDField(default=uuid.uuid4)
#     mobile_number = models.BigIntegerField(unique=True)
#     otp = models.CharField(max_length=8, null=True, blank=True)
#     Address = models.CharField(max_length=500,blank=False)
#     Otpcreated_at = models.DateTimeField(null=True, blank=True)
#     is_verified =models.BooleanField(default=False)
    

class CustomerRegistration(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=8, blank=False)
    uid = models.UUIDField(default=uuid.uuid4)
    mobile_number = models.BigIntegerField(unique=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    Address = models.CharField(max_length=500, blank=False)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    def save_otp_and_expiry(self):
        # Function to generate OTP and set its expiry time.
        current_time = timezone.now()
        if self.Otpcreated_at and self.Otpcreated_at > current_time:
            self.otp = str(random.randint(1000, 9999))
            self.Otpcreated_at = current_time + timezone.timedelta(minutes=60)
        else:
            self.otp = str(random.randint(1000, 9999))
            self.Otpcreated_at = current_time + timezone.timedelta(minutes=60)
        self.save()

    
        
    
#####################################################################


class CartItem(models.Model):
    user = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    product_name = models.ForeignKey(VendorArtwork, on_delete=models.CASCADE)
    #product_price = models.FloatField()
    product_quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

class PurchaseItem(models.Model):
    product_name = models.ForeignKey(VendorArtwork, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(default=0)
    

    
    