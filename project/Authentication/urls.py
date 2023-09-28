from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('account/register/', RegistrationAPIView.as_view()),
    # path('create/', AccountCreationAPIView.as_view()),
    path('account/login/', LoginAPIView.as_view()),
    path('account/oauth/', OAuthAPIView.as_view()),
    path('otp/email/send/', SendEmailOTP.as_view()),
    path('otp/email/verify/', VerifyEmailOTP.as_view()),
    path('otp/phone/send/', SendPhoneOTP.as_view()),
    path('otp/phone/verify/', VerifyPhoneOTP.as_view()),
    path('password/forget/', ForgetPassword.as_view()),
    
    # path('password/change/', ChangePassword.as_view()),
    # path('temp/', Temp.as_view()),
]