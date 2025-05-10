from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY'] = '2020325555825'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///eskomapp.db'



db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
login_manager = LoginManager(app)

login_manager.session_protection = 'strong'

login_manager.login_view = 'login'

from Reminderapp import routes
