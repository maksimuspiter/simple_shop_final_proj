# Generated by Django 4.2 on 2023-05-03 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_account_options_account_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='favorite_products',
            field=models.ManyToManyField(blank=True, related_name='account', to='shop.product'),
        ),
    ]