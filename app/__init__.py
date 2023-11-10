from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import mysql.connector
import os
import socket

ip_addres = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'User.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
UPLOAD_FOLDER = 'img'
UPLOAD_FILE = 'file'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FILE'] = UPLOAD_FILE
app.config['JSON_AS_ASCII'] = False

db_1 = SQLAlchemy(app)

try :
    db_2 = mysql.connector.connect(host=f'localhost',
                user='campkt',
                passwd='Jrnz,hm03',
                db="Campaign_KT")#)
                #ssl_disabled=True)
except:
    db_2 = mysql.connector.connect(host=f'{ip_addres}',
                user='campkt',
                passwd='Jrnz,hm03',
                db="Campaign_KT")#)
                #ssl_disabled=True)


migrate = Migrate(app, db_1)

login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'

from app import routes, model

