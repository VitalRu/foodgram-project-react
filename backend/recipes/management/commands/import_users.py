import csv

from django.core.management.base import BaseCommand

from recipes.models import User


PATH = '../data/'


class Command(BaseCommand):
    help = 'import data from ingredients.csv'

    def handle(self, *args, **kwargs):
        with open(f'{PATH}/example_users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                print(row)

                user, created = User.objects.get_or_create(
                    email=row[0],
                    username=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    password=row[4]
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'User {user.username} created'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'User {user.username} already exists'
                    ))

            self.stdout.write(self.style.SUCCESS(
                f'Data from {file.name} imported successfully'
            ))
