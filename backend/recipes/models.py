from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField('название ингредиента', max_length=200)
    measurement_unit = models.CharField('единица измерения', max_length=200)

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

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов"""

    name = models.CharField('имя тега', max_length=200)
    color = models.CharField(
        'HEX-цвет тега',
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#[0-9a-fA-F]{1,6}$',
                message='HEX color format only',
            )
        ]
    )
    slug = models.SlugField(
        'слаг тега',
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Invalid slug value',
            )
        ]
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
    )
    name = models.CharField(
        'название рецепта',
        max_length=200,
        unique=True,
    )
    image = models.ImageField(
        'изображение рецепта',
        upload_to='recipes/images',
        default=None,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        through='TagsInRecipe',
        verbose_name='тег рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientsInRecipe',
        verbose_name='ингредиенты рецепта',
    )
    text = models.TextField('Описание приготовления')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в мин.',
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=32_000)
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagsInRecipe(models.Model):
    """Модель для связи тегов с рецептами"""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag',
        verbose_name='Примененный тег'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='tag_recipe',
        verbose_name='Рецепт с данным тегом'
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
    """
    Модель для связи ингредиентов и рецептов. Имеет солбец amount для
    указания количества ингредиента в рецепте
    """

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент в рецепте'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(
        'количество ингредиента',
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
    """Модель для рецептов в избранном"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='пользователь избранного рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='рецепт в избранном'
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
    """Модель для добавления рецепта в сисок покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list',
        verbose_name='пользователь списка покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='рецепт в списке покупок'
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
