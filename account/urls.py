from django.urls import path
from account.views import*
from . import *
import channels.layers
from django.http import HttpResponse
from asgiref.sync import async_to_sync
channel_layer = channels.layers.get_channel_layer()


def xl(request):
    async_to_sync(channel_layer.group_send)(
    'new-name',
    {
        'type': 'chat_message',
        'message': "event_trigered_from_views"
    }
) 
    return HttpResponse("OK")
    
urlpatterns = [
    
    path("register/", Register.as_view(),name="register/"),
    # path("xl",xl),
    path("login/", Login.as_view(),name="login"),
    path("otp/", VerifyOtp.as_view(),name="otp"),
    path('SendPasswordResetEmail/',ResetPasswordSendEmailView.as_view(), name='sendpasswordresetemail'),
    path('reset-pasword/<uid>',SetNewPasswordView.as_view(),name='reset-password'),
    path("upload_profile", vendoreprofile.as_view(),name="profile"),
    path("upload_pentig", vendorartwork.as_view(),name="artwork"),
    path("Get_pentig/<int:id>", vendorartwork.as_view()),
    path("Get_pentig/", vendorartwork.as_view()),
    path("customerdata/", customerdetail.as_view()),
    path("customerdata/<int:id>", customerdetail.as_view()),
    # path("atc", AddToCart.as_view()),
    path("custumerRegister/",CustumerRegister.as_view(),name="custumerRegister"),
    path("clogin/",Customerlogin.as_view(),name="clogin"),
    path("cotp/", Cotpveryfiy.as_view(),name="otp"),

    ##################################################
    path('cart-items/', CartItemViews.as_view()), 
    path('get-cart-items/<int:id>', PurchaseItemView.as_view()),
    path('get-cart-items/', PurchaseItemView.as_view()),
    path('cartdelete/', CartPurchaseDelete.as_view()),
    path('cartdelete/<int:product_name_id>',CartPurchaseDelete.as_view()),
    #path('purchase/',PurchaseItemViews.as_view()),
    path('Delete-cart-items/<int:id>', DeleteCartitemViews.as_view()),
    # path('Put-cart-items/<int:id>', PutCartItemViews.as_view())
    path('forgot-password/', ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('reset_password/', ResetPasswordAPI.as_view(), name='reset_password'),
]









    
