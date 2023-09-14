from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            ),
        )


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#[0-9a-fA-F]{1,6}$',
                message='HEX color format only',
            )
        ]
    )
    slug = models.SlugField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Invalid slug value',
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipe',
        verbose_name='автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    image = models.ImageField(
        upload_to='recipes/images',
        default=None,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        through='TagsInRecipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientsInRecipe'
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagsInRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='tag_recipe'
    )

    class Meta:
        verbose_name = 'Теги в рецептах'
        verbose_name_plural = 'Теги в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='unique_tag_recipe'
            ),
        )


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецептах'
        verbose_name_plural = 'Ингдредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            ),
        )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Рецепты, избранное'
        verbose_name_plural = 'Рецепты, избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorited',
            ),
        )

    def __str__(self):
        return f'{self.user} added {self.recipe} to favorites'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_list'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list',
            ),
        )

    def __str__(self):
        return f'{self.user} added {self.recipe} to shopping list'
