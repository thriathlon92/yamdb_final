from django.core.mail import send_mail

CONFIRMATION_CODE_LEN = 10


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Регистрация на yamdb, код подтверждения',
        message='Спасибо за регистрацию в нашем сервисе. '
                f'Код подтверждения: {confirmation_code}',
        recipient_list=[email],
        fail_silently=False,
    )
