from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'app/static/img'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.form_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://action@localhost/action'
db = SQLAlchemy(app)

from app import views, models

app.config['SECRET_KEY'] = 'it works!'