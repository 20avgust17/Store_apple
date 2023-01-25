from django.core.mail import send_mail
from shop.celery import app
from store.models import Contact, Product


@app.task
def send_spam_email():
    product = Product.objects.get(id=12)
    for contact in Contact.objects.all():
        send_mail(
            'Вы подписаны на нашу рассылку новых товаров.',
            f'Теперь вам раз в две недели будет приходить самый выгодный товар, который есть в нашем магазине.'
            f' Сейчас в продаже имеется {product.title} имеет цену всего {product.price},' 
            f' настоятельно рекомендуем посмотреть, пока есть в наличии!',
            'ladinkodima@gmail.com',
            [contact.email],
            fail_silently=False

        )
