# Generated by Django 3.2 on 2023-12-14 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20231213_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useryamdb',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=20, verbose_name='Роль'),
        ),
    ]
