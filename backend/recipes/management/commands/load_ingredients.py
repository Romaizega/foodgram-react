import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from foodgram import settings

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):

        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv', 'r', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file)
            load_ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1])
                for row in csv_reader
            ]
            with transaction.atomic():
                Ingredient.objects.bulk_create(
                    load_ingredients)
            self.stdout.write(
                self.style.SUCCESS('Данные ingredients_csv загружены')
            )
