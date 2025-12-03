
## Установка Docker и Docker Compose на Windows

### 1. Установите Docker Desktop для Windows
```
https://docs.docker.com/desktop/setup/install/windows-install/
```

### 2. Проверьте установку
```
docker --version
docker compose version
```

## Установка проекта

### Клонируйте репозиторий
```
git clone https://github.com/icanstillhearyou/kursa4-pizza29.git
```
### Проверьте или создайте файлы: Docker, docker-compose.yml, nginx.conf
```
#Dockerfile
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \  
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn pizza29.wsgi:application --bind 0.0.0.0:8000"]
```
```
#docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  web:
    build: ./pizza29
    image: pizza29
    container_name: pizza29
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./pizza29:/app
    depends_on:
      db:
        condition: service_healthy
    command: sh -c "python manage.py migrate && gunicorn pizza29.wsgi:application --bind 0.0.0.0:8000"
    networks:
      - app-network

  nginx:
    image: nginx:latest
    container_name: nginx-server
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./pizza29/static:/app/static
      - ./pizza29/media:/app/media
    depends_on:
      - web
    networks:
      - app-network


volumes:
  postgres_data:
  static:
  media:

networks:
  app-network:
    driver: bridge
```
```
#Dockerfile
events {}

http {

    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    server {
        listen 80;
        #server_name localhost;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/static/;
        }

        location /media/ {
            alias /app/media/;
        }
    }
}
```
## Запуск проекта

### 1. Соберите и запустите контейнеры
```
docker compose up -d --build
```

### 2. Примените миграции базы данных (опционально)
```
docker compose exec web python manage.py migrate
```

### 3. Соберите статические файлы (опционально)
```
docker compose exec web python manage.py collectstatic --noinput
```

### 4. Создайте суперпользователя (опционально)
```
docker compose exec web python manage.py createsuperuser
```

### 5. Проверьте работу
Откройте браузер и перейдите по адресу:
- Основной сайт: http://localhost
- Админ-панель: http://localhost/admin

## Полезные команды

### Просмотр логов
```
# Все сервисы
docker compose logs -f

# Только Django
docker compose logs -f web

# Только Nginx
docker compose logs -f nginx

# Только PostgreSQL
docker compose logs -f db
```

### Остановка проекта
```
docker compose down
```

### Перезапуск проекта
```
docker compose restart
```

### Выполнение команд Django
```
# Любая management команда
docker compose exec web python manage.py <команда>

# Примеры:
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py shell
```

### Доступ к базе данных
```
docker compose exec db psql -U pizza29_user -d pizza29_db
```

## Полная очистка и пересборка

Если нужно полностью очистить проект:

```
# Остановить и удалить всё (включая volumes с данными!)
docker compose down -v --rmi all

# Пересоздать с нуля
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

## Структура проекта

```
pizza29/
├── docker-compose.yml      # Конфигурация Docker Compose
├── nginx.conf              # Конфигурация Nginx
├── .env                    # Переменные окружения (не коммитить!)
├── pizza29/                # Директория Django проекта
│   ├── Dockerfile          # Dockerfile для Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── pizza29/            # Настройки проекта
│   ├── cart/               # Приложение корзины
│   ├── main/               # Главное приложение
│   ├── orders/             # Приложение заказов
│   ├── payment/            # Приложение оплаты
│   ├── static/             # Статические файлы
│   ├── media/              # Медиа файлы
│   └── users/              # Приложение пользователей
└── README.md
```

## Решение проблем

### Проблема: CSS не загружается
```
# Очистите кэш браузера: Ctrl + Shift + R
# Проверьте статические файлы в контейнере nginx:
docker compose exec nginx ls -la /app/static/
```

### Проблема: Ошибка подключения к базе данных
```
# Проверьте статус контейнера БД:
docker compose ps

# Проверьте логи БД:
docker compose logs db
```

### Проблема: Контейнер web не запускается
```
# Проверьте логи:
docker compose logs web

# Убедитесь, что .env файл создан и заполнен
```

