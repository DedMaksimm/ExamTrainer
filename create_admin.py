import argparse
import getpass
import sys

from app import create_app, db
from app.models import User


def create_admin_user(email: str, password: str | None = None, username: str | None = None) -> None:
    """Создать пользователя-админа или обновить существующего."""
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()

        if user:
            user.is_admin = True
            if password:
                # Используем метод модели, если он есть
                try:
                    user.set_password(password)
                except Exception:
                    # Назначаем хеш прямо, если метода нет
                    from werkzeug.security import generate_password_hash
                    user.password_hash = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            print(f'Пользователь с email "{email}" обновлён: is_admin=True')
            if password:
                print('Пароль обновлён.')
            return

        # если пользователя нет — создаём нового
        if not username:
            username = email.split('@')[0]

        new_user = User(username=username, email=email, is_admin=True)
        if password:
            try:
                new_user.set_password(password)
            except Exception:
                from werkzeug.security import generate_password_hash
                new_user.password_hash = generate_password_hash(password)
        else:
            # попросим пароль интерактивно
            pw = getpass.getpass('Введите пароль для нового администратора: ')
            if not pw:
                print('Пароль не введён. Отмена.')
                return
            try:
                new_user.set_password(pw)
            except Exception:
                from werkzeug.security import generate_password_hash
                new_user.password_hash = generate_password_hash(pw)

        db.session.add(new_user)
        db.session.commit()
        print(f'Создан новый админ: {email}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Создать или обновить администратора (Flask app)')
    parser.add_argument('-e', '--email', help='Email администратора (например admin@example.com)')
    parser.add_argument('-p', '--password', help='Пароль (необязательно, если не передан – запросит интерактивно)')
    parser.add_argument('-u', '--username', help='Имя пользователя (если не указано, берётся часть до @)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if not args.email:
        args.email = input('Email администратора: ').strip()

    if not args.email:
        print('Email обязателен. Повторите запуск с --email или введите email при запросе.')
        sys.exit(1)

    create_admin_user(email=args.email, password=args.password, username=args.username)
