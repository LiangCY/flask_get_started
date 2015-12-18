# coding=utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:123456@localhost/test'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception, e:
            db.session.rollback()
            return e
        finally:
            return 0

    def is_existed(self):
        tem_user = User.query.filter_by(username=self.username, password=self.password).first()
        if tem_user is None:
            return 0
        else:
            return 1


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(32))
    content = db.Column(db.Text)

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception, e:
            db.session.rollback()
            return e
        finally:
            return 0


def get_all_entry():
    entry_list = Entry.query.filter_by().all()
    return entry_list
