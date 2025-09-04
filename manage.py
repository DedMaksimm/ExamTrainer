from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Question, Answer  # Импорт моделей, чтобы они были видны

app = create_app()
migrate = Migrate(app, db)

# Это нужно для команды flask db ...
if __name__ == '__main__':
    app.run()
