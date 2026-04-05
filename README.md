# Team Finder

## Стек

- Python 3.12+
- Django 6
- PostgreSQL
- Docker / Docker Compose

## Подготовка

```bash
cp .env_example .env
```

## Запуск 1: локально 

1. Установите зависимости:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Убедитесь, что в `.env`:

- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=5432`

3. Поднимите БД:

```bash
docker compose up -d db
```

4. Выполните миграции и запустите приложение:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте: `http://127.0.0.1:8000/projects/list`

## Запуск 2: полностью в Docker (приложение + PostgreSQL)

1. Соберите и запустите контейнеры:

```bash
docker compose up --build
```

2. Откройте приложение:

- `http://127.0.0.1:8000/projects/list`

3. Создайте суперпользователя (в отдельном терминале):

```bash
docker compose exec web python manage.py createsuperuser
```

Тестовые данные также создаются автоматически при старте контейнера (через `migrate`).

Демо-пользователи:
- `alice@example.com` (`Артем Степанов`) / `demo12345`
- `bob@example.com` (`Геннадий Горин`) / `demo12345`
- `carol@example.com` (`Марк Костя`) / `demo12345`

Если вы уже запускали проект раньше и хотите пересоздать БД с автозаполнением:

```bash
docker compose down -v
docker compose up --build
```

## Остановка

```bash
docker compose down
```