import os, click
from flask import Flask, render_template
from peewee import *
from flask_security import Security, PeeweeUserDatastore, login_required
from model import User, Publication, create_tables, drop_tables, database
from form import ExtendedRegisterForm
from flask_mail import Mail

app = Flask(__name__)
app.config['DEBUG']=True

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

user_datastore = PeeweeUserDatastore(database, User, '', '')

security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

"""Creation de la base de données"""
@app.cli.command()
def initdb():
    create_tables()
    click.echo('Initialisation de la Base de données')

"""Suppression de la base de données"""
@app.cli.command()
def dropdb():
    drop_tables()
    click.echo('Suppression de la Base de données')

@app.route('/')
@login_required
def skyblog():
    return render_template('skyblog.html')