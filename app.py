from flask import Flask
import os
from constant import Constant as CONSTANT

""" Initialize Flask app """
app = Flask(__name__, template_folder=os.path.abspath('templates'),
            static_folder=os.path.abspath('static'),
            static_url_path="")

with app.app_context():
    pass

if __name__ == '__main__':
    app.run(host=CONSTANT.API_HOST, port=CONSTANT.API_PORT, debug=True)
