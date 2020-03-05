from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import getenv
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "6424b0e72ff44c32600b68d0c9f9a3e5" #CHANGE BEFORE LAUNCH
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://tinokingstone:password@127.0.0.1/plug" #CHANGE BEFORE LAUNCH
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from plug_app import routes
