
---

## 🤖 Учебный Telegram-бот

Бот для записи на курсы, выдачи бесплатных гайдов и общения с пользователем.
Есть готовая база кнопок, возможность добавлять свои гайды/кнопки прямо в коде.

---

### 📦 1. Подготовка репозитория

```bash
git clone https://github.com/Dasakami/comtehno_bot.git
cd comtehno_bot
```

---

### ⚙️ 2. Переменные окружения

В проекте есть файл **`.env.example`** – скопируйте его в `.env` и заполните своими данными:

```bash
cp .env.example .env
```

**Обязательные параметры**:

| Переменная          | Описание                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| `BOT_TOKEN`         | Токен бота. Получить у [BotFather](https://t.me/BotFather)                                                    |
| `ADMIN_CHAT_IDS`    | ID админа через запятую. Узнать свой ID – [@userinfobot](https://t.me/userinfobot)                            |
| `POSTGRES_USER`     | Имя пользователя PostgreSQL                                                                                   |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL                                                                                             |
| `POSTGRES_DB`       | Имя базы данных                                                                                               |
| `DATABASE_URL`      | Полный DSN для SQLAlchemy/asyncpg.<br>Пример: `postgresql+asyncpg://postgres:1908@postgres:5432/comtehno_bot` |
| `REDIS_DSN`         | DSN для Redis (кэш/хранение состояний FSM). Пример: `redis://redis:6379/0`                                    |
| `WEBHOOK_URL`       | (Опционально) если используете вебхуки, укажите публичный URL                                                 |
| `SERVICE_HOST`      | Хост сервиса (по умолчанию `0.0.0.0`)                                                                         |
| `SERVICE_PORT`      | Порт (по умолчанию `8000`)                                                                                    |

---

### 📚 3. Статические гайды

Все готовые материалы хранятся в папке **`app/statics/`**

* Положите туда PDF/изображения/тексты.
* Кнопки и логику можно править в `app/keyboards.py` и хендлерах.

---

### 🚀 4. Запуск через Docker Compose (рекомендуется)

> Требуется установленный **Docker** и **docker-compose**.

1. Отредактируйте `.env`.
2. Поднимите сервисы:

```bash
docker compose up -d --build
```

3. Сервисы:

   * `bot` – основной контейнер бота (Python + aiogram)
   * `postgres` – база данных
   * `redis` – хранилище для FSM/кэша

После запуска бот автоматически стартует командой:

```bash
CMD ["python", "-m", "app.main"]
```

---

### ⚡ 5. Локальный запуск (без Docker)

1. Установите зависимости (Python 3.11+):

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

2. Убедитесь, что PostgreSQL и Redis запущены и соответствуют `.env`.
3. Запустите бота:

```bash
python -m app.main
```

---

### 💡 Дополнительно

* Для продакшна можно настроить **GitHub Actions** для автоматической сборки и деплоя на ваш сервер (например, VPS с Docker).
* Если нужна смена базы или кэша – редактируйте `.env` и пересобирайте контейнеры.

---