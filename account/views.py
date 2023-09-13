from django.contrib import messages
from rest_framework import status, response
from .serializers import*
from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import*
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import random
from django.utils import timezone
from datetime import timedelta
import os
# from django.shortcuts import get_object_or_404cls
from django.shortcuts import get_object_or_404
from .utils import send_message_to_socket
import random
from .models import CustomerRegistration
from .serializers import ForgotPasswordSerializer
from .serializers import ResetPasswordSerializer


######################################

def get_tokens_for_user(user):

    ''' THIS FUNCTION PROVIDE TOKEN CREATE MANUALLY '''

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Register(APIView):
    serializer_class = UserSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email=serializer.initial_data.get('email')
            serializer.save()
            user = vendorregistration.objects.get(email = email)
            current_time = timezone.now()
            if user.Otpcreated_at and user.Otpcreated_at > current_time:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            else:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            user.save()
            # send_otp_via_email(serializer.data['email'],user.otp)
            return Response({'id': str(user.id),"data": serializer.data,'otp':str(user.otp),'message': "Register successfully. sent otp on your email please check."},
                             status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOtp(APIView):
    serializer_class = VerifyOtpSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = vendorregistration.objects.filter(email=email).first()
            if not user:
                return Response({'message': "somthing went wrong","data": "invalid email"},
                             status=status.HTTP_400_BAD_REQUEST)
            current_time = timezone.now()
            if otp == user.otp and user.Otpcreated_at and user.Otpcreated_at > current_time:
                if user.otp == otp:
                    user.is_verifide =True
                    user.save()
                    # messages.add_message(request, messages.INFO,f"New vendor {user} is registered. Please approve.")
                    # return Response({'message': "Account is verifyd you can login account"},status=status.HTTP_201_CREATED)
                    message = f"New vendor {user} is registered. Please approve."
                    send_message_to_socket(message) # send message over web socket
                    messages.add_message(request, messages.INFO, message)
                    return Response({'message':message},status=status.HTTP_201_CREATED)
            return Response({'message': "Invalid Otp please try again","data": "wrong otp"},status=status.HTTP_400_BAD_REQUEST)    
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = serializer.initial_data.get('email')
        password = serializer.initial_data.get('password')
        user = vendorregistration.objects.filter(email=email).first()
        if not user:
            return Response({'message': "The vendor is not registered "}, status=status.HTTP_403_FORBIDDEN)
        if not user.Is_Approved:
            return Response({'message': "The vendor is registered but is awaiting approval"}, status=status.HTTP_403_FORBIDDEN)
        if user.email==email:
            if user.password==password:
                token = get_tokens_for_user(user)
                return Response({'id': str(user.id),'token':token,'message':'login success'},status=status.HTTP_200_OK)
            else:
                return response.Response({'errors':'Email or Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordSendEmailView(APIView):
    serializer_class = SendPasswordResetEmailSerializer 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email=serializer.initial_data.get('email')
        user = vendorregistration.objects.get(email=email)
        current_time = timezone.now()
        if user.Otpcreated_at and user.Otpcreated_at > current_time:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=1)
        else:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=1)
        user.save()
        send_otp_via_email_reset_password(email,user.otp)
        return Response({'uid': str(user.uid),'otp':str(user.otp),'message':"Otp send successfully"})
            

class SetNewPasswordView(APIView):
    serializer_class = UserPasswordResetSerializar
    def post(self, request, uid):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp =serializer.initial_data.get('otp')
            password =serializer.initial_data.get('password')
            password2 =serializer.initial_data.get('password2')
            profile = vendorregistration.objects.get(uid=uid)
            current_time = timezone.now()
            if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
                if otp == profile.otp:
                    if password == password2:
                        profile.password=password
                        profile.save()
                        return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'msg': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':"Invalid Otp please try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class vendoreprofile(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = VendorProfileSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        vendorid =int(serializer.initial_data.get('vendor'))
        print(vendorid)
        user = request.user.id
        if serializer.is_valid():    
            if vendorid == user:
                serializer.save()
                return Response({'data': serializer.data,'message':"profile created successfully"},status=status.HTTP_200_OK)
            else:
                return Response({'errors':"Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class vendorartwork(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = VendorArtworkSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        vendorid = int(serializer.initial_data.get('vendor'))
        user = request.user.id
        obj = VendorArtwork.objects.count()
        uploaded_file = serializer.initial_data.get('Art_image')
        max_size_in_bytes = 2 * 1024 * 1024  # 2 MB
        if serializer.is_valid():
            if vendorid == user:
                if obj <= 20:
                    if uploaded_file.size < max_size_in_bytes:
                        serializer.save()
                        print(obj)
                        return Response({'data': serializer.data,'message':" Artwork  uploaded successfully"},status=status.HTTP_200_OK)
                    else:
                        return Response({'message':" painting size more than 2Mb"},status=status.HTTP_200_OK)
                else:
                    return Response({'message':" painting upload limit over"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors':" Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self ,request,id=None):
        if id:
            penting = VendorArtwork.objects.get(id=id)
            serializer = VendorArtworkSerializer(penting)
            return Response({'data': serializer.data},status=status.HTTP_200_OK)

        penting_data = VendorArtwork.objects.all()
        serializer = VendorArtworkSerializer(penting_data, many=True)
        return Response({'data': serializer.data},status=status.HTTP_200_OK)
    

class customerdetail(APIView):
    serializer_class = customerSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':" pantting book successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self ,request, id=None):
        if id:
            data =customer.objects.get(id=id)
            serializer = customerSerializer(data)
            return Response({'data': serializer.data},status=status.HTTP_200_OK)

        data = customer.objects.all()
        serializer = customerSerializer(data, many=True)
        return Response({'data': serializer.data},status=status.HTTP_200_OK)


# class AddToCart(APIView):
    
#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             cart_item = serializer.validated_data
#             request.session.setdefault('cart_items', []).append(cart_item)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

#     def get(self, request):
#         cart_items = request.session.get('cart_items', [])
#         serializer = CartItemSerializer(cart_items, many=True)
#         return Response(serializer.data, status=200)
    


class CustumerRegister(APIView):
    serializer_class = CustumerRegisterSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email=serializer.initial_data.get('email')
            serializer.save()
            user = CustomerRegistration.objects.get(email = email)
            current_time = timezone.now()
            if user.Otpcreated_at and user.Otpcreated_at > current_time:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            else:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            user.save()
            send_otp_via_email(serializer.data['email'],user.otp)
           
            return Response({'id': str(user.id),"data": serializer.data,'otp':str(user.otp),'message': "Register successfully. sent otp on your email please check."},
                             status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    


class Cotpveryfiy(APIView):
    serializer_class = CustumerVerifyOtpSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = CustomerRegistration.objects.filter(email=email).first()
            if not user:
                return Response({'message': "somthing went wrong","data": "invalid email"},
                            status=status.HTTP_400_BAD_REQUEST)
            current_time = timezone.now()
            if otp == user.otp and user.Otpcreated_at and user.Otpcreated_at > current_time:
                if user.otp == otp:
                    user.is_verified =True
                    user.save()
                    messages.add_message(request, messages.INFO,f"New costumer {user} is registered. Please approve.")
                    return Response({'message': "Account is verifyd you can login account"},status=status.HTTP_201_CREATED)
            return Response({'message': "Invalid Otp please try again","data": "wrong otp"},status=status.HTTP_400_BAD_REQUEST)    
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Customerlogin(APIView):
    
    serializer_class = CustomerSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = serializer.initial_data.get('email')
        password = serializer.initial_data.get('password')
        user = CustomerRegistration.objects.filter(email=email).first()
        if not user:
            return Response({'message': "The Customer is not registered "}, status=status.HTTP_403_FORBIDDEN)
        if not user.is_verified:
            return Response({'message': "The Customer is registered but is awaiting approval"}, status=status.HTTP_403_FORBIDDEN)
        if user.email==email:
            if user.password==password:
                token = get_tokens_for_user(user)
                return Response({'id': str(user.id),'token':token,'message':'login success'},status=status.HTTP_200_OK)
            else:
                return response.Response({'errors':'Email or Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##############################################################################################################

class CartItemViews(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemSerializer
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class PurchaseItemView(APIView):
    def get(self, request, id=None):
        if id:
            item = CartItem.objects.get(id=id)
            serializer = CartItemSerializer(item) 
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PurchaseItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CartPurchaseDelete(APIView):
    def get(self, request,product_name_id=None):
        #item = CartItem.objects.get(product_name_id=product_name_id)
        item = CartItem.objects.filter(product_name_id=product_name_id).first()
        serializer = CartItemSerializer(item)
        CartItem.objects.filter(product_name_id=product_name_id).delete()
        return Response({"status": "Data Deleted success", "data": serializer.data}, status=status.HTTP_200_OK)
        

class DeleteCartitemViews(APIView):
    def delete(self, request,id=None):
        item = get_object_or_404(CartItem, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}) 
    
class PutCartItemViews(APIView):   
    def put(self, request, id=None):
        item = CartItem.objects.get(id=id)
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors}) 
        
        
        
###########################################################################################################        


#####forget######

class ForgotPasswordAPI(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = CustomerRegistration.objects.get(email=email)
            except CustomerRegistration.DoesNotExist:
                return Response({'message': "User with this email does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            current_time = timezone.now()
            if user.Otpcreated_at and user.Otpcreated_at > current_time:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            else:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=60)
            user.save()

            # Assuming you have a function to send OTP via email named 'send_otp_via_email'
            send_otp_via_email(email, user.otp)

            return Response({'id': str(user.id), 'email': email, 'otp': str(user.otp),
                             'message': "OTP has been sent to your email. Please check and use it to reset your password."},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 ###################reset password################

class ResetPasswordAPI(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            password = serializer.validated_data.get('password')
            
            try:
                user = CustomerRegistration.objects.get(email=email)
            except CustomerRegistration.DoesNotExist:
                return Response({'message': "User with this email does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            current_time = timezone.now()
            if user.Otpcreated_at and user.Otpcreated_at > current_time and str(user.otp) == otp:
                user.password = password
                user.save()
                return Response({'message': "Password reset successful."},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid OTP."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





