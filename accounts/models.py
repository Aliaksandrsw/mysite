import uuid

from PIL import Image
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class ExtendedUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    groups = models.ManyToManyField(
        'auth.Group', verbose_name='groups', blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='extended_user_set',
        related_query_name='extended_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', verbose_name='user permissions', blank=True,
        help_text='Specific permissions for this user.',
        related_name='extended_user_set',
        related_query_name='extended_user',
    )


class Profile(models.Model):
    user = models.OneToOneField(ExtendedUser, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
