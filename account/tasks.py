from celery import shared_task
from django.core.mail import send_mail
from decouple import config


@shared_task
def send_confirmation_mail(user, code):
    send_mail(
        subject='Письмо активации Unify',
        message='Введите данный код  в окно активации:'
        f'\n\n{code}\n'
        f'\nНикому не передавайте данный код!'
        '\n\n\nUnify test project',
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )


@shared_task
def send_password_reset(user, code):
    send_mail(
        subject='Письмо сброса пароля Unify',
        message='Никому не сообщайте данный код!\n'
                f'\n{code}\n\n'
                'Unify test project',
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )
