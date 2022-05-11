import logging
from flask import Flask
import os

from bugsnag.handlers import BugsnagHandler
from bugsnag.flask import handle_exceptions
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from constant import Constant as CONSTANT
from helper.endpoint_binder import bind_endpoints
from helper.log_helper import setup_logging

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


migrate = Migrate(app, db)

""" Initialize log """
setup_logging(log_path=CONSTANT.LOG_FILE_PATH)

""" Logger initialization """
logger = logging.getLogger(__name__)
handler = BugsnagHandler()

""" Send only ERROR-level logs and above """
handler.setLevel(logging.ERROR)
logger.addHandler(handler)

with app.app_context():
    """ Bind controller to Flask """
    bind_endpoints()

""" Attach Bugsnag to Flask's exception handler """
handle_exceptions(app)

if __name__ == '__main__':
    app.run(host=CONSTANT.API_HOST, port=CONSTANT.API_PORT, debug=CONSTANT.DEBUG_FLAG)
