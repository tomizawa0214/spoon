from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


GENDER_CHOICES = (
    ('1', '女性'),
    ('2', '男性'),
)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('お名前', max_length=30)
    furigana = models.CharField('フリガナ', max_length=30)
    email = models.EmailField('メールアドレス', unique=True)
    tel = models.CharField('電話番号', max_length=13)
    gender = models.CharField('性別', max_length=2, choices=GENDER_CHOICES, blank=True)
    birthday = models.DateField('誕生日', null=True, blank=True)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)