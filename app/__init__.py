from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pathlib


app = Flask(__name__,
            static_folder=pathlib.Path(__file__).parents[1] / 'web')
app.config.from_pyfile('../config.py')

login_manger = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# flask-uploads
uploader = UploadSet('uploads', IMAGES)
configure_uploads(app, uploader)


from app.model import *
from app.route import *


app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_comment, url_prefix='/comment')
app.register_blueprint(bp_post, url_prefix='/post')
