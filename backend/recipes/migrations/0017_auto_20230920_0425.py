# Generated by Django 3.2 on 2023-09-20 04:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20230920_0423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='HEX color format only', regex='^#[0-9a-fA-F]{1,6}$')], verbose_name='HEX-цвет тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='имя тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid slug value', regex='^[-a-zA-Z0-9_]+$')], verbose_name='слаг тега'),
        ),
    ]
