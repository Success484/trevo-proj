# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order, TrackingEvent
from django.conf import settings


@receiver(post_save, sender=Order)
def notify_receiver_on_order(sender, instance, created, **kwargs):
    """
    Send an email to the receiver only when a new Order is created.
    """
    if created:
        subject = f"New Order: {instance.tracking_number}"
        template = "emails/order_created.html"

        # Render HTML email template
        html_content = render_to_string(template, {"order": instance})
        text_content = strip_tags(html_content)  # fallback for plain-text clients

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email= settings.DEFAULT_FROM_EMAIL,  # update with your sender email
            to=[instance.receiver_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)



@receiver(post_save, sender=TrackingEvent)
def notify_receiver_on_tracking_event(sender, instance, created, **kwargs):
    """
    Send an email to the receiver only when a new TrackingEvent is created.
    """
    if created:
        subject = f"Package Update: {instance.order.tracking_number}"
        template = "emails/order_updated.html"

        # Render HTML email template
        html_content = render_to_string(template, {"event": instance, "order": instance.order})
        text_content = strip_tags(html_content)  # fallback for plain-text clients

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email= settings.DEFAULT_FROM_EMAIL,  # replace with your sender email
            to=[instance.order.receiver_email],      # get email from related Order
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)