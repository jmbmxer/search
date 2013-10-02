from flask_application import app

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    level = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))

class Links(db.Model):

    __tablename__='links'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    link = db.Column(db.String, unique=False, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    group = db.relationship('Groups', backref=db.backref('links', lazy='dynamic'))

    def __init__(self, author_id, link, group_id):
        self.author_id = author_id
        self.link = link
        self.group_id = group_id

    def __repr__(self):
        return'<Link %r>' %(self.link)


class Groups(db.Model):

    __tablename__="groups"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('groups', lazy = 'dynamic'))


    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


    def __repr__(self):
        return'<Name %r>'%(self.name)
