# Generated by Django 3.2 on 2023-09-20 04:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230920_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Invalid username!')], verbose_name='имя пользователя'),
        ),
    ]
