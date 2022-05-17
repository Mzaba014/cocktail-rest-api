from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """provides helper functions for creating users or super users"""

    def normalize_email(self, email: str) -> str:
        """Normalize email by lower-casing the domain part"""
        index = email.index('@')
        username = email[:index]
        domain = email[index:].lower()

        return username + domain

    def create_user(self, email: str, password: str):
        if email is None:
            raise ValueError("Email cannot be None")
        elif password is None:
            raise ValueError("Password cannot be None")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        """Leverage create_user to create a User, then modify the permission booleans and return the modified User"""
        user = self.create_user(email, password)
        print(type(user))
        user.is_superuser = True  # Boolean provided by PermissionsMixin, assigns full permissions to user
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model created by extending AbstractBaseUser and PermissionsMixin.

       ABU provides core implementation of User model such as hashed passwords
       PermissionsMixin provides db fields and methods for Django's permission model"""
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'  # the name of the field in the user model that is used as the unique identifier

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # allows access to admin panel

    objects = UserManager()


class Tag(models.Model):
    name = models.CharField(max_length=255)
    # set the submitted_by to the user who submits the tag. Remove all tags submitted by user on delete
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
