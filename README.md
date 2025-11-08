
# Django + PostgreSQL + Docker  
Инструкция по запуску проекта двумя способами:  
1) Через **готовые Docker-образы**, которые передаёшь другу.  
2) Через **GitHub**, где друг сам собирает контейнеры.

---

# 1. Структура проекта

```

project/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── src/

```

---

# 2. Файл `.env.example`

```

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

````

---

# 3. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
````

---

# 4. docker-compose.yml

```yaml
version: '3.9'

services:
  web:
    build: .
    container_name: django_app
    env_file:
      - .env
    command: python src/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: postgres_db
    env_file:
      - .env
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pg_data:
```

---

# 5. Инструкция для **тебя**: передача проекта через готовые образы

## 5.1 Собери образы

```
docker build -t my-django .
docker save my-django > django.tar
docker save postgres:16 > postgres.tar
```

## 5.2 Передай другу:

```
django.tar
postgres.tar
docker-compose.yml
.env.example -> .env
```

Друг создаёт `.env` вручную или копирует из примера.

---

# 6. Инструкция для **друга**, если он получил готовые образы

## 6.1 Загрузить образы

```
docker load < django.tar
docker load < postgres.tar
```

## 6.2 Создать файл `.env`

```
cp .env.example .env
```

## 6.3 Запустить контейнеры

```
docker-compose up
```

## 6.4 Выполнить миграции

```
docker-compose run web python src/manage.py migrate
```

## 6.5 Запуск приложения

```
docker-compose up
```

Доступ:
[http://localhost:8000](http://localhost:8000)

---

# 7. Инструкция для **друга**, если он скачал проект с GitHub

## 7.1 Склонировать репозиторий

```
git clone https://github.com/you/your-repo.git
cd your-repo
```

## 7.2 Создать `.env`

```
cp .env.example .env
```

## 7.3 Запустить сборку и запуск контейнеров

```
docker-compose up --build
```

## 7.4 Применить миграции

```
docker-compose run web python src/manage.py migrate
```

## 7.5 Запуск приложения

Если контейнеры были остановлены:

```
docker-compose up
```

Доступ:
[http://localhost:8000](http://localhost:8000)

---

# 8. Остановка контейнеров

```
docker-compose down
```

---

# 9. Примечания

1. `.env` не должен храниться в репозитории.
2. PostgreSQL-контейнер весит около 400 МБ, Django — 80–150 МБ.
3. Если нужно уменьшить размер образов, можно использовать более лёгкие Python-базы или SQLite для разработки.

