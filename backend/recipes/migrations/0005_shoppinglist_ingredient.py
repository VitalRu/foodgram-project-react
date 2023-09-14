# Generated by Django 4.2.4 on 2023-09-12 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_shoppinglist_shoppinglist_unique_shopping_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_to_buy', to='recipes.ingredient'),
            preserve_default=False,
        ),
    ]