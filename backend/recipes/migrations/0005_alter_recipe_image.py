# Generated by Django 4.2.4 on 2023-09-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredient_options_alter_tag_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, upload_to='recipes/images'),
        ),
    ]
