from app import create_app, db
from app.models import User, Question, Answer, Task, QuizSession, UserAnswer
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Question": Question,
        "Answer": Answer,
        "Task": Task,
        "QuizSession": QuizSession,
        "UserAnswer": UserAnswer,
    }

with app.app_context():
    db.create_all()
    print("База данных успешно инициализирована.")

