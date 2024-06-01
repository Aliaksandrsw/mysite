from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class VerifiedBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
            if user.is_verified:
                return user
            return None
        except UserModel.DoesNotExist:
            return None
