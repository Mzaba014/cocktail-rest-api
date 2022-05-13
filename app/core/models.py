from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """provides helper functions for creating users or super users"""

    def create_user(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model which allows email as username"""
    email = models.EmailField(max_length=254, unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'  # the name of the field in the user model that is used as the unique identifier
    is_admin = models.BooleanField(default=False)
