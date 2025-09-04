from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Question, Answer
from app.forms import LoginForm, RegisterForm, QuestionForm
from flask import render_template
from app import db
from app.data import fi_questions, algo_questions


main_bp = Blueprint("main", __name__)

# Главная страница
@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Страница регистрации
@main_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация прошла успешно. Теперь вы можете войти.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

# Страница входа
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы успешно вошли!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        else:
            flash("Неверный email или пароль", "danger")
    return render_template("login.html", form=form)

# Выход из системы
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("main.login"))

# Профиль пользователя
@main_bp.route('/profile')
@login_required
def profile():
    # берем попытки текущего пользователя
    user_id = int(current_user.get_id())
    sessions = QuizSession.query.filter_by(user_id=user_id).order_by(QuizSession.started_at.desc()).all()
    return render_template('profile.html', user=current_user, sessions=sessions)


# Список пользователей
@main_bp.route("/users")
@login_required
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)

from flask import request, flash

@main_bp.route('/questions/add', methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(text=form.text.data, question_type=form.question_type.data)
        for answer_form in form.answers:
            answer = Answer(
                text=answer_form.text.data,
                is_correct=answer_form.is_correct.data,
                order=answer_form.order.data if form.question_type.data == 'ordering' else None
            )
            question.answers.append(answer)
        db.session.add(question)
        db.session.commit()
        flash('Вопрос успешно добавлен!', 'success')
        return redirect(url_for('main.list_questions'))
    return render_template('add_question.html', form=form)
@main_bp.route('/questions')
@login_required
def list_questions():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template('list_questions.html', questions=questions)

@main_bp.route("/questions")
def questions():
    return render_template("questions.html")


@main_bp.route("/exam_questions")
def exam_questions():
    return render_template("exam_questions.html",
                           fi_questions=fi_questions,
                           algo_questions=algo_questions)


import os
import random
from datetime import datetime, timedelta
from flask import (
    render_template, redirect, url_for, flash, request, session, current_app, send_from_directory
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from app.forms import DemoStartForm, DemoExamForm, TaskUploadForm

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXT = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# ---- Демоэкзамен: старт (выбор) ----
@main_bp.route('/demo_exam', methods=['GET', 'POST'])
@login_required
def demo_exam_start():
    form = DemoStartForm()
    if form.validate_on_submit():
        exam_type = form.exam_type.data  # 'fi' или 'algo'
        # берем соответствующий массив вопросов (список словарей с key 'question', 'answer')
        pool = fi_questions if exam_type == 'fi' else algo_questions

        n = len(pool)
        if n < 2:
            flash('В пуле вопросов недостаточно вопросов для демоэкзамена.', 'danger')
            return redirect(url_for('main.index'))

        half = n // 2  # для 58 -> 29 и 29
        # первый вопрос из первой половины [0..half-1]
        idx1 = random.randrange(0, half)
        # второй вопрос из второй половины [half..n-1]
        idx2 = random.randrange(half, n)

        # сохраняем выбранные индексы и время старта в session
        session['demo_exam'] = {
            'exam_type': exam_type,
            'idx1': int(idx1),
            'idx2': int(idx2),
            'start_ts': datetime.utcnow().isoformat()
        }
        # длительность в секундах:
        session['demo_exam_duration'] = 45 * 60  # 2700 секунд

        return redirect(url_for('main.demo_exam_take'))

    return render_template('demo_start.html', form=form)

# ---- Демоэкзамен: прохождение ----
from datetime import datetime
from app.models import QuizSession, UserAnswer
from app.data import fi_questions, algo_questions

@main_bp.route('/demo_exam/take', methods=['GET', 'POST'])
@login_required
def demo_exam_take():
    data = session.get('demo_exam')
    if not data:
        flash('Сначала начните демоэкзамен.', 'warning')
        return redirect(url_for('main.demo_exam_start'))

    exam_type = data['exam_type']
    idx1 = int(data['idx1'])
    idx2 = int(data['idx2'])
    start_ts = datetime.fromisoformat(data['start_ts'])
    duration = int(session.get('demo_exam_duration', 45 * 60))
    elapsed = (datetime.utcnow() - start_ts).total_seconds()
    remaining = max(0, duration - int(elapsed))

    pool = fi_questions if exam_type == 'fi' else algo_questions

    q1 = {'question': pool[idx1]['question'], 'answer': pool[idx1].get('answer')}
    q2 = {'question': pool[idx2]['question'], 'answer': pool[idx2].get('answer')}

    form = DemoExamForm()
    if form.validate_on_submit():
        # Проверяем время серверно:
        elapsed = (datetime.utcnow() - start_ts).total_seconds()
        if elapsed > duration:
            flash('Время истекло — экзамен не засчитан.', 'warning')
            # можно всё же сохранить попытку с пометкой просроченной, но здесь мы отказали:
            return redirect(url_for('main.demo_exam_start'))

        # Создаём сессию в БД
        quiz_session = QuizSession(
            user_id=int(current_user.get_id()),
            exam_type=exam_type,
            started_at=start_ts,
            submitted_at=datetime.utcnow(),
            duration_seconds=duration
        )
        db.session.add(quiz_session)
        db.session.flush()  # получить id перед добавлением ответов

        # Сохраняем ответы пользователя, а также правильные ответы (на момент сдачи)
        ua1 = UserAnswer(
            session_id=quiz_session.id,
            question_index=idx1,
            question_text=q1['question'],
            correct_answer_text=q1.get('answer') or '',
            user_answer_text=form.answer1.data
        )
        ua2 = UserAnswer(
            session_id=quiz_session.id,
            question_index=idx2,
            question_text=q2['question'],
            correct_answer_text=q2.get('answer') or '',
            user_answer_text=form.answer2.data
        )
        db.session.add_all([ua1, ua2])
        db.session.commit()

        flash('Демоэкзамен сдан. Ответы сохранены.', 'success')
        return redirect(url_for('main.demo_exam_result', session_id=quiz_session.id))

    return render_template('demo_take.html', form=form, q1=q1, q2=q2, remaining=remaining, exam_type=exam_type)


# ---- Показ результата (сохранённой отправки) ----
@main_bp.route('/demo_exam/result_old/<int:sub_idx>')
@login_required
def demo_exam_result_old(sub_idx):
    subs = session.get('demo_submissions', [])
    if sub_idx < 0 or sub_idx >= len(subs):
        flash('Результат не найден.', 'danger')
        return redirect(url_for('main.index'))
    submission = subs[sub_idx]
    # Показываем вопрос + ответ (правильный ответ скрываем, т.к. у нас открытые)
    exam_type = submission['exam_type']
    pool = fi_questions if exam_type == 'fi' else algo_questions
    q1 = pool[submission['q1_index']]
    q2 = pool[submission['q2_index']]
    return render_template('demo_result.html', submission=submission, q1=q1, q2=q2)

# ---- упрощённая обработка авто-отправки при истечении, можно редиректить на take с сообщением ----
@main_bp.route('/demo_exam/submit')
@login_required
def demo_exam_submit():
    # если нужно, можно автоматически собрать значения из session (если они были)
    flash('Экзамен завершён.', 'info')
    return redirect(url_for('main.index'))


@main_bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@main_bp.route('/demo_exam/result/<int:session_id>')
@login_required
def demo_exam_result(session_id: int):
    qs = QuizSession.query.get_or_404(session_id)
    # доступ к чужим результатам запрещён
    if qs.user_id != int(current_user.get_id()):
        flash('Нет доступа к этой сессии.', 'danger')
        return redirect(url_for('main.profile'))

    answers = qs.answers  # list of UserAnswer (joined)
    return render_template('demo_result.html', session=qs, answers=answers)

import os
from datetime import datetime
from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models import Task, User

# --- admin_required ---
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.login"))
        if not getattr(current_user, "is_admin", False):
            flash("Доступ запрещён: требуется права администратора.", "danger")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    return decorated_view

# --- Конфиг для загрузки файлов (вставь в начало routes.py или create_app config) ---
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Список задач (всем пользователям доступно) ---
@main_bp.route("/tasks", methods=["GET"])
@login_required
def tasks():
    tasks_list = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=tasks_list)

# --- Страница добавления задачи (только админ) ---
@main_bp.route("/tasks/add", methods=["GET", "POST"])
@admin_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        file = request.files.get("file")

        if not title:
            flash("Введите заголовок задачи.", "warning")
            return redirect(url_for("main.add_task"))

        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.root_path, "static", "uploads", "tasks")
            os.makedirs(upload_dir, exist_ok=True)
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            filename_on_disk = f"{timestamp}_{filename}"
            file.save(os.path.join(upload_dir, filename_on_disk))
            # путь относительно static/
            file_path = f"uploads/tasks/{filename_on_disk}"
        elif file and file.filename:
            flash("Недопустимый тип файла. Разрешены: png, jpg, jpeg, gif, pdf.", "danger")
            return redirect(url_for("main.add_task"))

        task = Task(title=title, description=description, file_path=file_path, created_by=int(current_user.get_id()))
        db.session.add(task)
        db.session.commit()
        flash("Задача успешно добавлена.", "success")
        return redirect(url_for("main.tasks"))

    return render_template("add_task.html")

# --- Удаление задачи (только админ) ---
@main_bp.route("/tasks/delete/<int:task_id>", methods=["POST"])
@admin_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # удалить файл с диска, если есть
    if task.file_path:
        try:
            path = os.path.join(current_app.root_path, "static", task.file_path)
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            current_app.logger.exception("Ошибка при удалении файла задачи")
    db.session.delete(task)
    db.session.commit()
    flash("Задача удалена.", "info")
    return redirect(url_for("main.tasks"))

# --- Просмотр всех пользователей (только админ) ---
@main_bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users)











