from flask import Flask
import os
from constant import Constant as CONSTANT
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from helper.endpoint_binder import bind_endpoints

""" Initialize Flask app """
app = Flask(__name__, template_folder=os.path.abspath('templates'),
            static_folder=os.path.abspath('static'),
            static_url_path="")

app.config['SQLALCHEMY_DATABASE_URI'] = CONSTANT.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONSTANT.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["JWT_SECRET_KEY"] = CONSTANT.JWT_SECRET_KEY
jwt = JWTManager(app)

from models.models import db

db.init_app(app)

from models.models import Role, UserRole, User, Issue, Project,UserProfile,UserProject

migrate = Migrate(app, db)

with app.app_context():
    """ Bind controller to Flask """
    bind_endpoints()

if __name__ == '__main__':
    app.run(host=CONSTANT.API_HOST, port=CONSTANT.API_PORT, debug=True)
