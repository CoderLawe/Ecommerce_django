# Generated by Django 3.0.8 on 2021-03-19 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='slug',
        ),
    ]
