from flask import Flask
import os
from constant import Constant as CONSTANT
from flask_sqlalchemy import SQLAlchemy

""" Initialize Flask app """
app = Flask(__name__, template_folder=os.path.abspath('templates'),
            static_folder=os.path.abspath('static'),
            static_url_path="")

app.config['SQLALCHEMY_DATABASE_URI'] = CONSTANT.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

with app.app_context():
    pass

if __name__ == '__main__':
    app.run(host=CONSTANT.API_HOST, port=CONSTANT.API_PORT, debug=True)
