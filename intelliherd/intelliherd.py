from flask import Flask, request
from flask import render_template
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_restful import Resource, Api
import stripe


# Views
from views.public import public
from views.auth import auth 
from views.account import account
from views.farms import farms
from views.locations import locations
from views.organizations import orgs
from views.animals import animals
from views.pens import pens

# API
# v1
from api.v1.farm import apiFarm
from api.v1.animals import apiAnimals
from api.v1.relationships import apiRelationships

# Custom class imports
from models.objects import SystemUser, Base
from models.Connection import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfc\x123\xda\x06\xc8o\xf3\x95\x01\xafaU\\\xc1Z\xa4\xa9C\xddo\x020]'

db = SQLAlchemy(app)


# Blueprints
app.register_blueprint(public)
app.register_blueprint(auth)
app.register_blueprint(account)
app.register_blueprint(farms)
app.register_blueprint(locations)
app.register_blueprint(orgs)
app.register_blueprint(animals)
app.register_blueprint(pens)

# v1 API
app.register_blueprint(apiFarm)
app.register_blueprint(apiAnimals)
app.register_blueprint(apiRelationships)

# Flask Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Flask Mail
app.config['MAIL_SERVER']='somemail'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



@login_manager.user_loader
def load_user(user_id):
    return SystemUser.query.get(user_id)

Base.query = db_session.query_property()

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html', current_user=current_user)

# @app.route('/login')
# def login():
#     return render_template('login.html', current_user=current_user)

# @app.route('/lockscreen')
# def lockscreen():
#     return render_template('lockscreen.html', current_user=current_user)

@app.route('/empty')
@login_required
def empty():
    return render_template('empty.html', current_user=current_user)