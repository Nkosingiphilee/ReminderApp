from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SECRET_KEY'] = '2020325555825'

#db=SQLAlchemy(app)8from

from routes import*