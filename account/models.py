from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('The given email must be set!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True!')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True!')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=255)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,
                                        default='profile_pictures/default.png')
    profile_quote = models.CharField(max_length=255, default='Hey, I\'m new here!')
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    password_reset_code = models.CharField(max_length=255, blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} | {self.username}'

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code
