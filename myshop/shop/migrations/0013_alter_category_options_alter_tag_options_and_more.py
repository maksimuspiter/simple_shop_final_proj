# Generated by Django 4.2 on 2023-05-04 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_comment_customer_delete_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['slug'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['slug'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.RemoveIndex(
            model_name='category',
            name='shop_catego_name_289c7e_idx',
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['slug'], name='shop_catego_slug_5ac49f_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['slug'], name='shop_tag_slug_c44279_idx'),
        ),
    ]
