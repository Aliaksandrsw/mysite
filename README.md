# Блог-сайт на Django

Это блог-сайт на основе Django с расширенными функциями, включая Celery для управления задачами, социальную аутентификацию и документацию API.

## Особенности

- Создание и управление записями блога
- Аутентификация пользователей и вход через социальные сети
- Celery для обработки фоновых задач
- RESTful API с использованием Django Rest Framework
- Документация API с помощью drf-spectacular
- Система тегов для записей блога
- Поддержка базы данных PostgreSQL

## Требования

Этот проект построен на Python и Django. Основные зависимости включают:

- Django 5.0.6
- Celery 5.4.0
- Django Rest Framework 3.15.1
- PostgreSQL (через psycopg 3.1.19)
- Pillow 10.3.0 для обработки изображений
- django-celery-beat 2.6.0 для планирования задач
- social-auth-app-django 5.4.1 для социальной аутентификации

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Unix или MacOS: `source venv/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Настройте базу данных PostgreSQL
6. Примените миграции: `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер разработки: `python manage.py runserver`

## Использование

- Административная панель доступна по адресу `/admin/`
- API документация доступна по адресу `/api/schema/swagger-ui/`

## Настройка Celery

1. Установите и настройте Redis
2. Запустите Celery worker: `celery -A your_project_name worker -l info`
3. Для периодических задач запустите: `celery -A your_project_name beat -l info`




