# Generated by Django 4.2.4 on 2023-09-12 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_remove_shoppinglist_unique_shopping_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shopping_list', to=settings.AUTH_USER_MODEL),
        ),
    ]