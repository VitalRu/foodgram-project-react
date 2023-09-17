import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag


PATH = '../data/'


class Command(BaseCommand):
    help = 'import data from ingredients.csv'

    def handle(self, *args, **kwargs):
        with open(f'{settings.BASE_DIR}/data/tags.csv', 'r',) as file:
            reader = csv.reader(file)

            for row in reader:
                print(row)

                tag, created = Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Tag {tag.name} created'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Tag {tag.name} already exists'
                    ))

            self.stdout.write(self.style.SUCCESS(
                f'Data from {file.name} imported successfully'
            ))
