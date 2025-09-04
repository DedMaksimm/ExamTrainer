# app/auth/routes.py
from typing import Dict, Any
from flask import Blueprint, redirect, url_for, session, request, current_app, flash
from authlib.integrations.flask_client import OAuthError
from app import oauth, db
from app.models import User
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login/<provider>")
def oauth_login(provider: str):
    client = oauth.create_client(provider)
    if not client:
        flash("OAuth provider not configured.", "danger")
        return redirect(url_for("main.login"))

    redirect_uri = url_for("auth.oauth_callback", provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)


@auth_bp.route("/callback/<provider>")
def oauth_callback(provider: str):
    """
    Callback от провайдера: получаем токен и инфо о пользователе, создаём/логиним.
    """
    client = oauth.create_client(provider)
    if not client:
        flash("OAuth provider not configured.", "danger")
        return redirect(url_for("main.login"))

    try:
        token = client.authorize_access_token()
    except OAuthError:
        flash("Не удалось получить токен от провайдера.", "danger")
        return redirect(url_for("main.login"))


    try:
        resp = client.get("userinfo")  # для google
        user_info = resp.json()
    except Exception:
        resp = client.get("https://login.yandex.ru/info")
        user_info = resp.json()

    email = user_info.get("email") or user_info.get("default_email")
    sub = user_info.get("id") or user_info.get("sub") or user_info.get("uid")

    if not email:
        flash("Провайдер не вернул email — регистрация невозможна.", "danger")
        return redirect(url_for("main.login"))

    # попытаемся найти пользователя по email
    user = User.query.filter_by(email=email).first()
    if user is None:
        # создать нового
        username = email.split("@")[0]
        user = User(username=username, email=email, oauth_provider=provider, oauth_id=sub)
        # пароль не устанавливаем — вход через OAuth
        db.session.add(user)
        db.session.commit()
    else:
        # если есть, можно связать, если ещё не связан
        if not user.oauth_provider:
            user.oauth_provider = provider
            user.oauth_id = sub
            db.session.commit()

    login_user(user)
    flash("Вход выполнен через " + provider.capitalize(), "success")
    return redirect(url_for("main.index"))
