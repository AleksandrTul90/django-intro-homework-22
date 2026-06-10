"""
Генерация скриншотов для задания 5 (Django shell).
Запуск: python scripts/generate_shell_screenshots.py
Требуется настроенная PostgreSQL и применённые миграции.
"""
import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
SCREENSHOTS_DIR.mkdir(exist_ok=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(BASE_DIR))

import django

django.setup()

from catalog.models import Category, Product


def run_shell_session():
    lines = ['$ python manage.py shell', '']
    namespace = {'Category': Category, 'Product': Product}

    def capture(command, code):
        lines.append(f'In [1]: {command}')
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exec(code, namespace)
        output = buffer.getvalue().strip()
        if output:
            lines.append(output)
        if '_result' in namespace:
            lines.append(repr(namespace.pop('_result')))
        lines.append('')

    Category.objects.all().delete()
    Product.objects.all().delete()

    capture(
        'Category.objects.create(name="Смартфоны", description="Мобильные телефоны")',
        'Category.objects.create(name="Смартфоны", description="Мобильные телефоны")',
    )
    capture(
        'Category.objects.create(name="Ноутбуки", description="Портативные компьютеры")',
        'Category.objects.create(name="Ноутбуки", description="Портативные компьютеры")',
    )
    capture(
        'smartphones = Category.objects.get(name="Смартфоны")',
        'smartphones = Category.objects.get(name="Смартфоны")',
    )
    capture(
        'Product.objects.create(name="iPhone 15", description="Смартфон Apple", category=smartphones, price=89990)',
        'Product.objects.create(name="iPhone 15", description="Смартфон Apple", category=smartphones, price=89990)',
    )
    capture(
        'Product.objects.create(name="Samsung Galaxy S24", description="Смартфон Samsung", category=smartphones, price=74990)',
        'Product.objects.create(name="Samsung Galaxy S24", description="Смартфон Samsung", category=smartphones, price=74990)',
    )
    capture(
        'laptops = Category.objects.get(name="Ноутбуки")',
        'laptops = Category.objects.get(name="Ноутбуки")',
    )
    capture(
        'Product.objects.create(name="MacBook Air", description="Ноутбук Apple", category=laptops, price=119990)',
        'Product.objects.create(name="MacBook Air", description="Ноутбук Apple", category=laptops, price=119990)',
    )
    capture(
        'list(Category.objects.all())',
        '_result = list(Category.objects.all())',
    )
    capture(
        'list(Product.objects.all())',
        '_result = list(Product.objects.all())',
    )
    capture(
        'list(Product.objects.filter(category=smartphones))',
        '_result = list(Product.objects.filter(category=smartphones))',
    )
    capture(
        'product = Product.objects.get(name="iPhone 15"); product.price = 84990; product.save(); product.price',
        'product = Product.objects.get(name="iPhone 15"); product.price = 84990; product.save(); _result = product.price',
    )
    capture(
        'Product.objects.get(name="Samsung Galaxy S24").delete()',
        'Product.objects.get(name="Samsung Galaxy S24").delete()',
    )
    capture(
        'list(Product.objects.all())',
        '_result = list(Product.objects.all())',
    )

    return lines


def render_terminal_image(lines, filename, title):
    font_path = Path('C:/Windows/Fonts/consola.ttf')
    font = ImageFont.truetype(str(font_path), 16) if font_path.exists() else ImageFont.load_default()
    title_font = ImageFont.truetype(str(font_path), 18) if font_path.exists() else ImageFont.load_default()

    line_height = 22
    padding = 20
    width = 1200
    height = padding * 2 + 30 + len(lines) * line_height

    image = Image.new('RGB', (width, height), '#1e1e1e')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 32), fill='#323232')
    draw.text((padding, 6), title, fill='#ffffff', font=title_font)

    y = padding + 20
    for line in lines:
        if line.startswith('In ['):
            color = '#4ec9b0'
        elif line.startswith('$'):
            color = '#569cd6'
        else:
            color = '#d4d4d4'
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    image.save(SCREENSHOTS_DIR / filename)


def main():
    lines = run_shell_session()

    sections = [
        ('01_create_data.png', 'Django Shell — создание категорий и продуктов', 0, 16),
        ('02_all_categories.png', 'Django Shell — получение всех категорий', 16, 20),
        ('03_all_products.png', 'Django Shell — получение всех продуктов', 20, 24),
        ('04_products_by_category.png', 'Django Shell — продукты определённой категории', 24, 28),
        ('05_update_price.png', 'Django Shell — обновление цены продукта', 28, 32),
        ('06_delete_product.png', 'Django Shell — удаление продукта и проверка', 32, len(lines)),
    ]

    header = lines[:2]
    for filename, title, start, end in sections:
        render_terminal_image(header + lines[start:end], filename, title)
        print(f'Создан: {SCREENSHOTS_DIR / filename}')


if __name__ == '__main__':
    main()
