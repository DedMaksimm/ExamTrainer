from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Подтвердите пароль",
        validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')]
    )
    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FieldList, FormField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    text = StringField('Текст ответа', validators=[DataRequired()])
    is_correct = BooleanField('Правильный ответ')
    order = IntegerField('Порядок (для сортировки)', default=0)

class QuestionForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    question_type = SelectField('Тип вопроса', choices=[('multiple_choice', 'Выбор из вариантов'), ('open', 'Открытый ответ'), ('ordering', 'Порядок')], validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=2, max_entries=10)
    submit = SubmitField('Добавить вопрос')

from wtforms import SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class DemoStartForm(FlaskForm):
    exam_type = SelectField(
        'Выберите экзамен',
        choices=[('fi', 'Фундаментальная информатика'), ('algo', 'Алгоритмы и структуры данных')],
        validators=[DataRequired()]
    )
    start = SubmitField('Начать Демоэкзамен')

class DemoExamForm(FlaskForm):
    answer1 = TextAreaField('Ответ на вопрос 1', validators=[DataRequired()])
    answer2 = TextAreaField('Ответ на вопрос 2', validators=[DataRequired()])
    submit = SubmitField('Сдать экзамен')

class TaskUploadForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired()])
    description = TextAreaField('Описание (опционально)')
    file = FileField('Файл задачи (опционально)', validators=[FileAllowed(['pdf','txt','png','jpg','zip'], 'Только документы/изображения/архивы')])
    upload = SubmitField('Загрузить задачу')





