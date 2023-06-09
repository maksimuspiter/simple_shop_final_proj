# Generated by Django 4.2 on 2023-05-04 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('orders', '0003_alter_order_customer'),
        ('shop', '0011_alter_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_comments', to='account.account', verbose_name='Автор комментария'),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
