# Generated by Django 4.2.4 on 2023-09-12 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_shoppinglist_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppinglist',
            name='ingredient',
        ),
    ]