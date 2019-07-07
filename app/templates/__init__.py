from flask import Flask
from flask_nav import Nav
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GaanaProject.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
Bootstrap(app)
nav = Nav(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import views
