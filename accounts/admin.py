from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile, ExtendedUser
from django.contrib import admin

admin.site.register(Profile)


@admin.register(ExtendedUser)
class ExtendedUserAdmin(UserAdmin):
    pass