# Generated by Django 4.2 on 2023-05-09 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_message_creator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AddField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=False, verbose_name='Просмотрено'),
        ),
        migrations.AlterField(
            model_name='message',
            name='creator',
            field=models.CharField(choices=[('U', 'User'), ('A', 'Admin')], default='A', max_length=1, verbose_name='Автор сообщения'),
        ),
    ]