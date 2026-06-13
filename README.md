# Интернет-магазин на Django

Учебный проект интернет-магазина в рамках курса «Знакомство с Django».

## Описание

Базовая структура интернет-магазина на Django: главная страница каталога и страница контактов с формой обратной связи. Проект использует PostgreSQL, модели `Category` и `Product`, админ-панель, фикстуры и кастомную команду загрузки данных.

## Технологии

- Python 3
- Django 6
- PostgreSQL
- Bootstrap 5
- Pillow, ipython, python-dotenv

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone <url-репозитория>
cd <название-проекта>
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте базу данных PostgreSQL в pgAdmin (например, `catalog_db`).

5. Скопируйте шаблон переменных окружения и укажите параметры подключения к БД:

```bash
copy .env.example .env
```

6. Примените миграции:

```bash
python manage.py migrate
```

7. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

8. Загрузите тестовые данные (опционально):

```bash
python manage.py load_catalog_data
```

9. Запустите сервер разработки:

```bash
python manage.py runserver
```

10. Откройте в браузере:

- Главная страница: http://127.0.0.1:8000/
- Контакты: http://127.0.0.1:8000/contacts/
- Админ-панель: http://127.0.0.1:8000/admin/

## Структура проекта

```
.
├── catalog/                    # Приложение каталога
│   ├── fixtures/               # Фикстуры категорий и продуктов
│   ├── management/commands/    # Кастомные команды
│   ├── migrations/             # Миграции БД
│   ├── templates/              # HTML-шаблоны
│   ├── admin.py                # Настройки админки
│   ├── models.py               # Модели Category и Product
│   ├── urls.py
│   └── views.py
├── config/                     # Настройки Django-проекта
├── screenshots/                # Скриншоты Django shell (задание 5)
├── .env.example                # Шаблон переменных окружения
├── manage.py
├── requirements.txt
└── README.md
```

## GitFlow

- `main` — стабильная ветка
- `develop` — ветка разработки
- `homework/*` — ветки для домашних заданий

Домашние задания сдаются через pull request из ветки домашней работы в `develop`.

## Автор

Учебный проект курса «Знакомство с Django».
