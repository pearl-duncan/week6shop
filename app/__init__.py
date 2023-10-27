from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS

#import blueprints
from .auth import auth

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(auth)


db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page!'
login_manager.login_message_category = 'danger'

from . import routes