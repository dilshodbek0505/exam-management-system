from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta

from celery import shared_task

from .utils import create_url

User = get_user_model()



@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id = user_id)
    
    expired_date = timezone.now() + timedelta(hours=1)
    verification_url = create_url({
        "id": str(user.id),
        "expired_date": expired_date.timestamp() 
    })
    
    verification_url = f"http://127.0.0.1:8000/api/v1/user/verification/email/{verification_url}/"

    subject = "Verify your email address"
    html_message = render_to_string('emails/verification_email.html', {
        'username': user.username,
        'verification_url': verification_url
    })

    from_email = settings.DEFAULT_FROM_EMAIL
    user_email_list = [user.email]

    send_mail(subject, '', from_email, user_email_list, html_message=html_message)

