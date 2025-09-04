# ExamTrainer

## 🚀 Краткое описание

ExamTrainer — веб‑приложение на Flask, позволяющее готовиться к экзаменам: создавать аккаунты, тренироваться, входить через Google и Yandex. Проект спроектирован как стартовая база: понятная структура, Flask Blueprints, SQLAlchemy и поддержка миграций.

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
| БД                       | SQLite (по умолчанию для разработки), поддержка PostgreSQL и т.д. |
| Миграции                 | Flask-Migrate (Alembic)                                           |
| Управление зависимостями | Poetry (рекомендуется)                                            |
| Файловая структура       | Blueprints (main, auth), моделирование через SQLAlchemy           |

---

## 👥 Команда

Даже если проект маленький, важно указать роли — у нас команда из одного человека:

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
git clone <REPO_URL>
cd exam_trainer

# устанавливаем зависимости
poetry install

# создаём файл .env (см. пример ниже)
# инициализация миграций (только при первом запуске)
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

1. Форкните репозиторий
2. Создайте ветку: `git checkout -b feature/your-feature`
3. Сделайте изменения, закоммитьте и отправьте PR

---

## 📄 Лицензия

Moscow Aviation Institute © Максимов Максим

---




