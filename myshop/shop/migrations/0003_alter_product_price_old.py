# Generated by Django 4.2 on 2023-04-21 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_alter_product_options_product_price_old"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price_old",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
