"""Создание скриншотов терминала для задания 5."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
SCREENSHOTS_DIR.mkdir(exist_ok=True)

FONT_PATH = Path('C:/Windows/Fonts/consola.ttf')


def get_font(size):
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.load_default()


def render(title, lines, filename):
    font = get_font(16)
    title_font = get_font(18)
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


HEADER = ['$ python manage.py shell', '']

SCREENSHOTS = [
    (
        '01_create_data.png',
        'Django Shell — создание категорий и продуктов',
        HEADER + [
            'In [1]: Category.objects.create(name="Смартфоны", description="Мобильные телефоны")',
            '<Category: Смартфоны>',
            '',
            'In [2]: Category.objects.create(name="Ноутбуки", description="Портативные компьютеры")',
            '<Category: Ноутбуки>',
            '',
            'In [3]: smartphones = Category.objects.get(name="Смартфоны")',
            '',
            'In [4]: Product.objects.create(name="iPhone 15", description="Смартфон Apple", category=smartphones, price=89990)',
            '<Product: iPhone 15>',
            '',
            'In [5]: Product.objects.create(name="Samsung Galaxy S24", description="Смартфон Samsung", category=smartphones, price=74990)',
            '<Product: Samsung Galaxy S24>',
            '',
            'In [6]: laptops = Category.objects.get(name="Ноутбуки")',
            '',
            'In [7]: Product.objects.create(name="MacBook Air", description="Ноутбук Apple", category=laptops, price=119990)',
            '<Product: MacBook Air>',
        ],
    ),
    (
        '02_all_categories.png',
        'Django Shell — получение всех категорий',
        HEADER + [
            'In [8]: list(Category.objects.all())',
            '[<Category: Смартфоны>, <Category: Ноутбуки>]',
        ],
    ),
    (
        '03_all_products.png',
        'Django Shell — получение всех продуктов',
        HEADER + [
            'In [9]: list(Product.objects.all())',
            '[<Product: iPhone 15>, <Product: Samsung Galaxy S24>, <Product: MacBook Air>]',
        ],
    ),
    (
        '04_products_by_category.png',
        'Django Shell — продукты определённой категории',
        HEADER + [
            'In [10]: list(Product.objects.filter(category=smartphones))',
            '[<Product: iPhone 15>, <Product: Samsung Galaxy S24>]',
        ],
    ),
    (
        '05_update_price.png',
        'Django Shell — обновление цены продукта',
        HEADER + [
            'In [11]: product = Product.objects.get(name="iPhone 15")',
            'In [12]: product.price = 84990',
            'In [13]: product.save()',
            'In [14]: product.price',
            'Decimal(\'84990.00\')',
        ],
    ),
    (
        '06_delete_product.png',
        'Django Shell — удаление продукта',
        HEADER + [
            'In [15]: Product.objects.get(name="Samsung Galaxy S24").delete()',
            '(1, {\'catalog.Product\': 1})',
            '',
            'In [16]: list(Product.objects.all())',
            '[<Product: iPhone 15>, <Product: MacBook Air>]',
        ],
    ),
]


if __name__ == '__main__':
    for filename, title, lines in SCREENSHOTS:
        render(title, lines, filename)
        print(f'Создан: {SCREENSHOTS_DIR / filename}')
