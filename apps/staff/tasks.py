from django.core.mail import send_mail
from django.conf import settings

from oa_backend import celery_app


@celery_app.task(name='send_mail_task')
def send_mail_task(email, subject, message):
    send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
