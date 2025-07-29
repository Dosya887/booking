from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .choices import MyUserRoleEnum # Убедитесь, что это правильный импорт, если choices.py в той же папке

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email), # Используйте normalize_email для приведения email к нижнему регистру
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Создает и сохраняет суперпользователя с указанным именем пользователя, email и паролем.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True # Если у вас есть поле is_admin, как флаг суперпользователя
        user.is_staff = True # Django админка требует это
        user.is_superuser = True # Требуется для is_superuser
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(max_length=255, verbose_name="Почта", unique=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='Аватар')
    role = models.CharField(max_length=123,
                            verbose_name='Роль',
                            choices=MyUserRoleEnum.choices,
                            default=MyUserRoleEnum.STANDARD_USER)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12 ,verbose_name='Баланс')

    # Добавьте необходимые поля для совместимости с админкой Django и суперпользователями
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Нужно для доступа к админке
    is_superuser = models.BooleanField(default=False) # Нужно для прав суперпользователя
    is_admin = models.BooleanField(default=False) # Если вы используете это как свой флаг админа


    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # Методы, необходимые для Django админки и разрешений
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin # Или self.is_superuser, если is_admin - это просто синоним

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin # Или self.is_superuser


class Email2FACode(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, verbose_name='6-значный код')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.code}"