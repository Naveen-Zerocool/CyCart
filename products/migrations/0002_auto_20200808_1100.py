# Generated by Django 2.2.15 on 2020-08-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0, help_text='Discount amount on cart'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, help_text='Price of all products on cart'),
        ),
    ]
