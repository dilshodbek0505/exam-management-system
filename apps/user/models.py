from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from apps.common.models import BaseModel



class User(AbstractUser, BaseModel):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class UserRole(models.TextChoices):
        student = 'student', _('Student')
        admin = 'admin', _('Admin')

    role = models.CharField(max_length=64, choices=UserRole.choices, default='student', verbose_name=_('Role'))

    
    class Meta(AbstractUser.Meta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        swappable = "AUTH_USER_MODEL"
