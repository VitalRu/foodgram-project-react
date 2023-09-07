# from django.db import models
# from django.core.validators import RegexValidator
# from users.models import User


# class Ingredient(models.Model):
#     name = models.CharField(
#         max_length=200,
#         unique=True
#     )
#     measurement_unit = models.CharField(
#         max_length=200,
#         verbose_name='Единица измерения'
#     )

#     class Meta:
#         ordering = ['name']

#     def __str__(self):
#         return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=True)
#     color = models.CharField(
#         max_length=7,
#         validators=[
#             RegexValidator(
#                 regex=r'^#[0-9a-fA-F]{6}$',
#                 message='Цвет должен быть в формате HEX',
#             )
#         ]
#     )
#     slug = models.SlugField(
#         max_length=255,
#         validators=[
#             RegexValidator(
#                 regex=r'^[-a-zA-Z0-9_]+$',
#                 message='Недопустимое значение slug',
#             )
#         ]
#     )


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         User,
#         related_name='recipe',
#         verbose_name='автор рецепта',
#     )
#     name = models.CharField(
#         max_length=200,
#         unique=True,
#     )
#     image = models.ImageField(
#         upload_to='images/recipes',
#         default=None,
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         through='TagRecipe',
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='IngredientsInRecipe'
#     )
#     text = models.TextField()
#     cooking_time = models.PositiveIntegerField()
