from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY'] = '2020325555825'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///eskomapp.db'

#app.config['UPLOAD_FOLDER'] = 'static/uploads'# Set upload folder
import os

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}  # Set allowed file types

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'Phungulankosingiphile828@gmail.com'

app.config['MAIL_PASSWORD'] =""


db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
login_manager = LoginManager(app)


mail = Mail(app)
login_manager.session_protection = 'strong'

login_manager.login_view = 'login'

from Reminderapp import routes
