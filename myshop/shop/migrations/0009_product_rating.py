# Generated by Django 4.2 on 2023-05-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_account_favorite_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]