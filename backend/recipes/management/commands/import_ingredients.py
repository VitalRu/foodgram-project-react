import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


PATH = '../data/'


class Command(BaseCommand):
    help = 'import data from ingredients.csv'

    def handle(self, *args, **kwargs):
        with open(f'{PATH}/ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)

                ingredient, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Ingredient {ingredient.name} created'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Ingredient {ingredient.name} already exists'
                    ))

            self.stdout.write(self.style.SUCCESS(
                f'Data from {file.name} imported successfully'
            ))
