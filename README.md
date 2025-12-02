
## Установка Docker и Docker Compose на Ubuntu

### 1. Обновите систему
```
sudo apt update
sudo apt upgrade -y
```

### 2. Установите зависимости
```
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

### 3. Добавьте официальный репозиторий Docker
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 4. Установите Docker
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 5. Добавьте текущего пользователя в группу docker
```
sudo usermod -aG docker $USER
newgrp docker
```

### 6. Проверьте установку
```
docker --version
docker compose version
```

## Установка проекта

### 1. Клонируйте репозиторий
```
git clone <URL_вашего_репозитория>
cd pizza29
```

### 2. Создайте файл .env

Создайте файл `.env` в корневой директории проекта со следующим содержимым:

```
# PostgreSQL Database
POSTGRES_DB=pizza29_db
POSTGRES_USER=pizza29_user
POSTGRES_PASSWORD=your_secure_password_here

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Connection
DB_NAME=pizza29_db
DB_USER=pizza29_user
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=5432
```

**⚠️ Важно:** Замените `your_secure_password_here` и `your-secret-key-here` на свои значения!

### 3. Создайте SECRET_KEY для Django

Сгенерируйте новый SECRET_KEY:
```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Скопируйте полученный ключ и вставьте в `.env` файл.

## Запуск проекта

### 1. Соберите и запустите контейнеры
```
docker compose up -d --build
```

### 2. Примените миграции базы данных
```
docker compose exec web python manage.py migrate
```

### 3. Соберите статические файлы
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

