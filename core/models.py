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
    genero_choices = (('Masculino', 'Masculino'), ('Feminino', 'Feminino'))
    email = models.EmailField(
        max_length=255, null=True, blank=False, unique=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True, unique=True)
    genero = models.CharField(
        max_length=9, choices=genero_choices, null=True, blank=True)
    # profile_image = models.ImageField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=13, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    pais = models.CharField(max_length=255, null=True, blank=True)
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
        return self.nome

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


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Animal(BaseModel):
    especie_choices = (('Cachorro', 'Cachorro'), ('Gato', 'Gato'))
    idade_choices = (('Filhote', 'Filhote'), ('Adulto', 'Adulto'), ('Idoso', 'Idoso'))
    porte_choices = (('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande'))

    name = models.CharField(null=True, blank=True, max_length=30)
    apelido = models.CharField(null=True, blank=True, max_length=30)
    especie = models.CharField(null=True, blank=True, max_length=10)
    idade = models.CharField(null=True, blank=True, max_length=30)
    porte = models.CharField(null=True, blank=True, max_length=30)
    castrado = models.BooleanField(default=False)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)
    contato = models.CharField(null=True, blank=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['id']

    def __str__(self):
        return str(self.name)
