from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет существующие данные и загружает тестовые категории и продукты из фикстур'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('Существующие данные удалены.'))

        call_command('loaddata', 'categories', 'products')
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены.'))
