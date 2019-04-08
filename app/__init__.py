from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_restful import Api
import pathlib


app = Flask(__name__,
            static_folder=pathlib.Path(__file__).parents[1] / 'web')
app.config.from_pyfile('../config.py')

login_manger = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

# flask-uploads
uploader = UploadSet('uploads', IMAGES)
configure_uploads(app, uploader)


from app.model import *
from app.route import *


app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_comment, url_prefix='/comment')
app.register_blueprint(bp_post, url_prefix='/post')

api.add_resource(Notices, '/notice')
api.add_resource(Notice, '/notice/<int:nid>')


from flask_restful import Resource
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/test')
