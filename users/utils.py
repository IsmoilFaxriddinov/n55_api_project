import random
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.models import VerificationModel


def get_verification_code(user):
    code = random.randint(1000, 9999)
    user_code = VerificationModel.objects.filter(user=user, code=code)
    if user_code.exists():
        user_code.delete()
        get_verification_code(user=user)
    
    VerificationModel.objects.create(user=user, code=code, expire_minutes=1)
    return code


def send_email_confirmation(user, code):
    subject = "Confirm Your Email Address"
    
    html_message = render_to_string(
        template_name='auth/email_confirmation.html',
        context={
            'user': user,
            'code': code,
        }
    )

    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.content_subtype = 'html'
    email.send()
