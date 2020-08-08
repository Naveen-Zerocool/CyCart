# Generated by Django 2.2.15 on 2020-08-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200808_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total price of the item based on quantity', max_digits=6),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price of the product', max_digits=6),
        ),
    ]