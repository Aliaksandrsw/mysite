from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token
from mysite.tasks import send_verification_email
from .models import Profile, ExtendedUser


@receiver(post_save, sender=ExtendedUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=ExtendedUser)
def set_is_active(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.is_active = True
        instance.save()


@receiver(post_save, sender=ExtendedUser)
def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)