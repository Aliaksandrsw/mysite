from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token

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
        send_mail(
            'Verify your  account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            'admin@localhost.ru',
            [instance.email],
            fail_silently=False,
        )
