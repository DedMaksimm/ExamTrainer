# ExamTrainer

## 🚀 Краткое описание

ExamTrainer — интерактивный тренажёр для подготовки к экзаменам, созданное, чтобы превратить боталку в понятный и приятный процесс.
Быстрая регистрация, личный кабинет, тренировки и вход через Google / Yandex — всё, чтобы готовиться эффективно и без лишних настроек.

---

## ✨ Возможности веб‑приложения

* Регистрация и вход по email/паролю
* Вход через OAuth (Google, Yandex)
* Управление пользователями (создание, поиск, авторизация)
* Хранение данных в реляционной БД (SQLAlchemy + Flask‑Migrate)
* Простая архитектура с blueprints (`main`, `auth`) — легко расширять
* Лёгкая локальная настройка через `.env`

---

## 🧰 Технологический стек

| Слой                     | Технологии / библиотеки                                           |
| ------------------------ | ----------------------------------------------------------------- |
| Бэкенд                   | Python 3.10+, Flask, Flask-Login, Flask-Migrate, Flask-SQLAlchemy |
| OAuth                    | Authlib (authlib.integrations.flask\_client)                      |
| БД                       | SQLite, поддержка PostgreSQL и т.д. |
| Миграции                 | Flask-Migrate (Alembic)                                           |
| Управление зависимостями | Poetry                                             |
| Файловая структура       | Blueprints (main, auth), моделирование через SQLAlchemy           |

---

## 👥 Команда


| Роль                | Участник        |
| ------------------- | --------------- |
| Team Lead           | Максимов Максим |
| Backend             | Максимов Максим |
| Frontend            | Максимов Максим |
| DevOps / Deployment | Максимов Максим |
| Дизайн / UI         | Максимов Максим |


---

## ⚙️ Быстрая установка (локально)

Требования: Python 3.10+, Poetry (или используйте venv + pip).

```bash
# клонируем репозиторий
git clone <https://github.com/DedMaksimm/ExamTrainer>
cd exam_trainer

# устанавливаем зависимости
poetry install

# создаём файл .env 
# инициализация миграций
poetry run flask db init
poetry run flask db migrate -m "Init"
poetry run flask db upgrade

# запуск приложения
poetry run flask run --host=127.0.0.1 --port=5000
# или
poetry run python run.py
```

Откройте в браузере: `http://127.0.0.1:5000`

---

## 🗂 Cтруктура проекта

```
exam_trainer/
├─ app/
│  ├─ __init__.py
│  ├─ extensions.py
│  ├─ models.py
│  ├─ routes.py
│  └─ auth/
│     ├─ __init__.py
│     └─ routes.py
├─ migrations/
├─ .env
├─ run.py
├─ pyproject.toml
└─ README.md
```

---

## 🤝 Как внести вклад

Нашли баг или есть идея?
Создайте issue или пишите на maksimov.maksim06@gmail.com — отвечаем быстро 😉

---

## 📄 Лицензия

Moscow Aviation Institute © Максимов Максим

---




