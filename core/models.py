from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class UserManager(BaseUserManager):
    """_summary_

    Args:
        BaseUserManager (_type_): _description_
    """

    def create_user(self, email, password=None):
        """_summary_

        Args:
            email (_type_): _description_
            password (_type_, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not email:
            raise ValueError(_('Users must have an email'))

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """_summary_

        Args:
            email (_type_): _description_
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """_summary_

    Args:
        AbstractBaseUser (_type_): _description_

    Returns:
        _type_: _description_
    """
    genre_choices = (('M', 'Masculino'), ('F', 'Feminino'))
    email = models.EmailField(
        max_length=255, null=True, blank=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=False, unique=True)
    genre = models.CharField(
        max_length=255, choices=genre_choices, null=True, blank=True)
    # profile_image = models.ImageField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    cellphone = models.CharField(max_length=13, null=True, blank=True)
    zipcode = models.CharField(max_length=9, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    complement = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    forgot_password_hash = models.CharField(
        max_length=255, null=True, blank=True)
    forgot_password_expire = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.name

    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """_summary_

        Args:
            perm (_type_): _description_
            obj (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return True

    def has_module_perms(self, app_label):
        """_summary_

        Args:
            app_label (_type_): _description_

        Returns:
            _type_: _description_
        """
        return True

    def is_verified(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.is_active

    @property
    def is_staff(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.is_admin
