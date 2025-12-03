
## Установка Docker и Docker Compose на Windows

### 1. Установите Docker Desktop для Windows
```
https://docs.docker.com/desktop/setup/install/windows-install/
```

### 2. Проверьте установку
```
docker --version
docker-compose version
```

## Установка проекта

### Клонируйте репозиторий
```
git clone https://github.com/icanstillhearyou/kursa4-pizza29.git
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

