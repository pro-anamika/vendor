from rest_framework import serializers
from .models import *
# import os

################################

# class OtpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Otp
#         fields = ('id', 'phone_number', 'otp_code', 'is_approved', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =vendorregistration
        fields = ['name','email','password']


class VerifyOtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    class Meta:
            model =vendorregistration
            fields = ['email','otp']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorregistration
        fields =['email','password']



class SendPasswordResetEmailSerializer(serializers.ModelSerializer):  
    class Meta:
        model = vendorregistration
        fields = ['email']



class UserPasswordResetSerializar(serializers.Serializer):
    
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        model =vendorregistration
        fields = ['otp','password','password2']
        

class VendorProfileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = VendorProfile
        fields = ['vendor','name','profile_picture','age','city','working_or_studying']  

class VendorArtworkSerializer(serializers.ModelSerializer):  
    class Meta:
        model = VendorArtwork
        fields = ['id','vendor', 'Art_image','themes','price','medium','description']
        

class customerSerializer(serializers.ModelSerializer):  
    class Meta:
        model = customer
        fields = ['id','panting', 'name','email','mobile_number','Address']   


class CartItemSerializer(serializers.Serializer):
    panting = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    

class CustumerRegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomerRegistration
        fields = ['id','email','password', 'name','mobile_number','Address']   


class CustumerVerifyOtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    class Meta:
            model = CustomerRegistration
            fields = ['email','otp']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRegistration
        fields =['email','password']

# #######################################

class CartItemSerializer(serializers.ModelSerializer):
    product_name = models.CharField(max_length=200)
    #product_price = models.FloatField()
    class Meta:
        model = CartItem
        fields = ['user','product_name']

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['product_name']


################################################

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

 
 
 ###################reset password################

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=4, max_length=4)
    password = serializers.CharField(min_length=8, write_only=True)
 


