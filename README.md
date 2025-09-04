# ExamTrainer

> **A lightweight exam preparation trainer built with Flask** — supports local registration and OAuth sign-in (Google and Yandex). Copy the contents below into your project's `README.md`.

---

## 🚀 Features

* Email/password registration and login
* OAuth login (Google, Yandex)
* SQLAlchemy ORM + Flask-Migrate for database management
* Simple blueprint-based structure (`main`, `auth`)

---

## ⚙️ Quickstart (local development)

Prerequisites: Python 3.10+, [Poetry](https://python-poetry.org/) (or use `pip`/venv if you prefer).

```bash
# clone the repo
git clone <REPO_URL>
cd exam_trainer

# install dependencies
poetry install

# create .env (see example below)
# initialize database migrations (first run only)
poetry run flask db init
poetry run flask db migrate -m "Init"
poetry run flask db upgrade

# run the app
poetry run flask run --host=127.0.0.1 --port=5000
# or
poetry run python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🔐 Example `.env`

```.env
SECRET_KEY=replace_with_a_strong_secret
DATABASE_URL=sqlite:///app.db
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
YANDEX_CLIENT_ID=
YANDEX_CLIENT_SECRET=
```

> For production use a real database (Postgres, MySQL) and HTTPS.

---

## 🔁 OAuth setup (Google & Yandex)

**Important:** The redirect URI you register in the provider console must match exactly the one produced by Flask's `url_for(..., _external=True)` (scheme, host, port and path).

### Typical local redirect URIs

If you run the app at `http://127.0.0.1:5000`, register these callbacks in provider settings:

```
http://127.0.0.1:5000/auth/callback/google
http://127.0.0.1:5000/auth/callback/yandex
```

If you use `localhost` or a different port, the string must match precisely.

---

## 🧱 Models (User)

Important fields used in the app (example model):

```py
from datetime import datetime
from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=True)  # nullable=True for OAuth users
    is_admin = db.Column(db.Boolean, default=False)
    oauth_provider = db.Column(db.String(50), nullable=True)
    oauth_id = d
```
