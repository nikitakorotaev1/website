from ..extensions import db
from flask_login import LoginManager
from ..models.data import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Пока не работает

