from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name=_("avatar"))
