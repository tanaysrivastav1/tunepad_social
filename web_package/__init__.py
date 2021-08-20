from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secret'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#tunepad is ROLE***
#postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tunepad:tanay@localhost:5432/tunepad"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from web_package import routes

