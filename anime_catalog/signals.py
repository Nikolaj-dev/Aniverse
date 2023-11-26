from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from anime_catalog.models import Comment
from .tasks import send_comment_notification_task


@receiver(post_save, sender=Comment)
def send_comment_reply_notification(sender, instance, created, **kwargs):
    if created and instance.parent:
        subject = 'You have received a response to your comment'
        message = f"There is a response to your comment:\n\n{instance.text}\n\n" \
                  f"To view the response, click on the following link:\n" \
                  f"http://127.0.0.1:8000{reverse('comment-detail', args=[instance.id])}\n\n" \
                  "Thank you for participating in the discussion!"

        recipient_email = instance.user.user.email

        send_comment_notification_task.delay(subject, message, recipient_email)
