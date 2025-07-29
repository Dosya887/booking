from django.db.models import TextChoices

class MyUserRoleEnum(TextChoices):
    STANDARD_USER = 'standard'
    MANAGER = 'manager'
    ADMIN = 'admin'