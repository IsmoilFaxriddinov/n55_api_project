from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse

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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

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
