# Generated by Django 2.2.15 on 2020-08-08 10:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='If the entry is active or soft deleted')),
                ('price', models.PositiveSmallIntegerField()),
                ('discount', models.PositiveSmallIntegerField()),
                ('user', models.OneToOneField(blank=True, help_text='If logged in user, then Cart will be saved against this User', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='If the entry is active or soft deleted')),
                ('title', models.CharField(help_text='Title of the product', max_length=64)),
                ('description', models.TextField(help_text='Description of the product')),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of the product', max_digits=6)),
                ('image', models.URLField(blank=True, help_text='Image for the product', null=True)),
                ('stock', models.IntegerField(blank=True, help_text='Stock available for the product', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'product',
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='If the entry is active or soft deleted')),
                ('quantity', models.PositiveSmallIntegerField(default=1, help_text='Quantity of the item on cart', validators=[django.core.validators.MinValueValidator(1)])),
                ('cart', models.ForeignKey(help_text='To which cart this item is associated with', on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='products.Cart')),
                ('product', models.ForeignKey(help_text='Associated product on the cart', on_delete=django.db.models.deletion.CASCADE, related_name='cart_product', to='products.Product')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'db_table': 'cart_item',
                'get_latest_by': 'created_at',
            },
        ),
    ]
