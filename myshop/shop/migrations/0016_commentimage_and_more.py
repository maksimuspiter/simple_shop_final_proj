# Generated by Django 4.2 on 2023-05-12 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_comment_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='comment_img/%Y/%m/%d', verbose_name='Фото')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.comment', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Отзыв о товаре',
                'verbose_name_plural': 'Отзывы о товаре',
                'ordering': ['created'],
            },
        ),
        migrations.AddIndex(
            model_name='commentimage',
            index=models.Index(fields=['created'], name='shop_commen_created_e7cada_idx'),
        ),
        migrations.AddIndex(
            model_name='commentimage',
            index=models.Index(fields=['comment'], name='shop_commen_comment_ba124f_idx'),
        ),
    ]
