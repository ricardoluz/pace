# Generated by Django 4.2.14 on 2024-08-25 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_usersystem_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersystem',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
