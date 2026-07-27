Дипломный проект: Веб-сайт для аренды одежды
Наталья Бажина
логин на GitHub - tasha137@mail.ru
e-mail — tasha137@mail.ru

# Платформа аренды одежды

Веб-приложение на Django для размещения объявлений об аренде одежды, поиска вещей, бронирования на нужные даты и оставления отзывов.

## Features / Technologies / Setup

| Раздел | Содержимое |
| --- | --- |
| **Features** | Объявления с фото, поиск по фильтрам, бронирование, отзывы, модерация, личный кабинет, аутентификация |
| **Technologies** | Python, Django, PostgreSQL, Docker, HTML, CSS |
| **Setup** | Установка зависимостей, миграции, запуск через Python или Docker |

## Возможности

- Размещение объявления с описанием, ценой, местоположением, контактами и фотографиями.
- Поиск по заголовку, описанию, местоположению и стоимости аренды.
- Редактирование и удаление собственных объявлений.
- Бронирование вещи на выбранные даты.
- Раздел «Мои брони».
- Отзывы об объявлениях и продавцах.
- Модерация объявлений перед публикацией.
- Авторизация пользователей для доступа к бронированию и контактам.

## Запуск проекта

### Локально
```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Через Docker
```bash
docker-compose up --build
```

Если нужны миграции:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Админ-панель

Админ-панель доступна по адресу `/admin`.  
Через неё можно модерировать объявления и управлять данными проекта.
