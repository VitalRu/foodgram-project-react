# Generated by Django 4.2.4 on 2023-09-14 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_alter_tag_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tagsinrecipe',
            options={'verbose_name': 'Теги в рецептах'},
        ),
    ]
