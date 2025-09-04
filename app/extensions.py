# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()


from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
