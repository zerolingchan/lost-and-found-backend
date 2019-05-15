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


access_control_allow_origin = [
    # 'http://localhost:8080',
    'https://zerolingchan.github.io'
    # 'https://zerolingchan.github.io/lost-and-found-fronten',
]

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', ','.join(access_control_allow_origin))
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


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
api.add_resource(User, '/user/<int:uid>')

api.add_resource(Comments, '/comment')
api.add_resource(Comment, '/comment/<int:cid>')

api.add_resource(Posts, '/post')
api.add_resource(Post, '/post/<int:pid>')

api.add_resource(Notices, '/notice')
api.add_resource(Notice, '/notice/<int:nid>')
api.add_resource(Search, '/search')
