from django.core.mail import send_mail
from django.conf import settings


def send_otp_via_email(email,otp):
    subject = 'your account verification email'
    message = f'your otp is {otp} '
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])

def send_otp_via_email_reset_password(email,otp):
    subject = 'your account reset password email'
    message = f'your otp is {otp} '
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])



# def send_otp_via_email_login(email,otp):
#     subject = 'your account verification email'
#     message = f'your otp is {otp} '
#     email_from = settings.EMAIL_HOST
#     send_mail(subject, message, email_from, [email])

