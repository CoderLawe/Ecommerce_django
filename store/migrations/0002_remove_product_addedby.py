# Generated by Django 3.0.8 on 2021-03-11 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='addedby',
        ),
    ]
