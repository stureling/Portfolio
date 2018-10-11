from flask_login import LoginManager, login_user, login_required, UserMixin
import data

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    # Database file of all the users and their passwords
    users = data.load_users("users.json")

    # Start Flask-Login
    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
