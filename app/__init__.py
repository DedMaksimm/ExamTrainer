from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os
from .extensions import db, migrate

load_dotenv()  # подгружаем .env

db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()

def create_app():
    app = Flask(__name__)

    # Настройки из .env
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "devkey"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    oauth.init_app(app)

    # регистрируем OAuth провайдеров
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v2/",
        client_kwargs={"scope": "openid email profile"},
        userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo"
    )

    oauth.register(
        name="yandex",
        client_id=os.getenv("YANDEX_CLIENT_ID"),
        client_secret=os.getenv("YANDEX_CLIENT_SECRET"),
        access_token_url="https://oauth.yandex.com/token",
        authorize_url="https://oauth.yandex.com/authorize",
        api_base_url="https://login.yandex.ru/",
        client_kwargs={"scope": "login:info login:email"},
        userinfo_endpoint="https://login.yandex.ru/info"  # Yandex ID docs.
    )


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


