# Generated by Django 4.2 on 2023-05-05 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_comment_customer'),
        ('account', '0004_account_activated_cupon_alter_account_cupons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cupons',
            field=models.ManyToManyField(blank=True, null=True, related_name='accounts', to='shop.cupon', verbose_name='Доступные купоны'),
        ),
        migrations.AlterField(
            model_name='account',
            name='favorite_products',
            field=models.ManyToManyField(blank=True, null=True, related_name='account', to='shop.product', verbose_name='Избранные продукты'),
        ),
    ]
