from aniverse.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def send_comment_notification_task(subject, message, recipient_email):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

