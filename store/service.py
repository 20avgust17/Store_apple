from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписали на нашу рассылку',
        'Мы будем присылать вам 5 новых товаров каждую неделю!',
        'ladinkodima@gmail.com',
        [user_email],
        fail_silently=False,
    )