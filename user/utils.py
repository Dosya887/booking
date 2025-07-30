import random
from .models import Email2FACode, MyUser
from django.core.mail import send_mail



def send_2fa_code(user):
    code = str(random.randint(100000, 999999))
    Email2FACode.objects.update_or_create(user=user, defaults={'code': code})

    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код для входа: {code}',
        from_email='tdastan.312@gmail.com',
        recipient_list=[user.email],
        fail_silently=False
    )
