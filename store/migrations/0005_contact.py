# Generated by Django 4.1.4 on 2023-01-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.EmailField(max_length=50)),
                ('last_name', models.EmailField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]
