"""
Модели базы данных для проекта Exam Trainer.
Формат докстрингов — NumpyDoc, аннотации типов присутствуют.
"""

from datetime import datetime
from typing import Optional

from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    """Модель пользователя.

    Parameters
    ----------
    db.Model : SQLAlchemy declarative base
    UserMixin : mixin для flask-login
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  
    oauth_provider = db.Column(db.String(50), nullable=True)
    oauth_id = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        """Хешировать и сохранить пароль.

        Parameters
        ----------
        password : str
            Пароль в открытом виде.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверить пароль.

        Parameters
        ----------
        password : str
            Пароль в открытом виде.

        Returns
        -------
        bool
            True, если пароль совпадает с хешем.
        """
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship("Answer", backref="question", cascade="all, delete-orphan", lazy="select")


class Answer(db.Model):
   

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, nullable=True)


class QuizSession(db.Model):
    

    __tablename__ = "quiz_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_type = db.Column(db.String(20), nullable=False)  # 'fi' или 'algo'
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Integer, default=45 * 60)

    user = db.relationship("User", backref=db.backref("quiz_sessions", lazy="dynamic"))

    def __repr__(self) -> str:
        return f"<QuizSession id={self.id} user_id={self.user_id} exam_type={self.exam_type}>"


class UserAnswer(db.Model):


    __tablename__ = "user_answers"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("quiz_sessions.id"), nullable=False)
    question_index = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer_text = db.Column(db.Text, nullable=True)
    user_answer_text = db.Column(db.Text, nullable=True)

    session = db.relationship(
        "QuizSession",
        backref=db.backref("answers", cascade="all, delete-orphan", lazy="joined"),
    )

    def __repr__(self) -> str:
        return f"<UserAnswer id={self.id} session_id={self.session_id} q_idx={self.question_index}>"

class Task(db.Model):
    """Задача с файлом-ответом (картинка/пдф)."""
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(300), nullable=True)  
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", backref=db.backref("created_tasks", lazy="dynamic"))

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"



