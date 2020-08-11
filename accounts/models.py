from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.mail import send_mail
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
    email = models.EmailField('メールアドレス', max_length=256, unique=True)
    tel = models.CharField('電話番号', max_length=13)
    gender = models.CharField('性別', max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField('誕生日', null=True, blank=True)

    is_staff = models.BooleanField(
        ('管理サイト使用権限'),
        default=False,
        help_text=('ユーザーがこの管理サイトにログインできるかどうかを指定します。'),
    )
    is_active = models.BooleanField(
        ('アクティブ判定'),
        default=True,
        help_text=(
            'このユーザーをアクティブとして扱うかどうかを指定します。 '
            'アカウントを削除する代わりに、これを選択解除します。'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('会員一覧')
        verbose_name_plural = ('会員一覧')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)