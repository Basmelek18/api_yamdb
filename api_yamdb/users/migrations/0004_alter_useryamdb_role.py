# Generated by Django 3.2 on 2023-12-14 18:17

from django.db import migrations, models
import users.enums


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_useryamdb_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useryamdb',
            name='role',
            field=models.CharField(choices=[('admin', 'ADMIN'), ('user', 'USER'), ('moderator', 'MODERATOR')], default=users.enums.UserRole['USER'], max_length=20, verbose_name='Роль'),
        ),
    ]