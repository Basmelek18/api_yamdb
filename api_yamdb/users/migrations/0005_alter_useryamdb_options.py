# Generated by Django 3.2 on 2023-12-14 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_useryamdb_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useryamdb',
            options={'ordering': ('last_name', 'first_name'), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
