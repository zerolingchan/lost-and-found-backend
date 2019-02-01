from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('../config.py')
login_manger = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.model import *
from app.route import *


app.register_blueprint(bp_user, url_prefix='/user')
