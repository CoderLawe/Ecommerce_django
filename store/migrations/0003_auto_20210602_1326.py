# Generated by Django 3.0.8 on 2021-06-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_detailed_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(choices=[('Phones', 'Phones'), ('Computers', 'Computers'), ('Accesories', 'Accesories')], default='Gen', max_length=200),
        ),
    ]