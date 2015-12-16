# coding=utf-8
from flask import Flask, request, url_for, render_template, flash, abort

from model import *

from wtforms import Form, StringField, PasswordField, validators, TextAreaField

import base64
import random
import time

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def hello_world():
    content = "Hello world!"
    return render_template('index.html', content=content)


@app.route('/user')
def hello_user():
    user = User(1, 'lcy')
    return render_template('user.html', user=user)


@app.route('/users')
def user_list():
    users = []
    for i in range(1, 10):
        user = User(i, 'user' + str(i))
        users.append(user)
    return render_template('user_list.html', users=users)


@app.route('/user/<id>')
def get_user(id):
    if int(id) == 1:
        user = User(1, 'lcy')
        return render_template('user_id.html', user=user)
    else:
        abort(404)


@app.route('/query_user')
def query_user():
    id = request.args.get('id')
    return 'query user ' + id


@app.route('/page/1')
def page_1():
    return render_template('page_1.html')


@app.route('/page/2')
def page_2():
    return render_template('page_2.html')


@app.route('/query_url')
def query_url():
    return 'query url: ' + url_for('query_user')


class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    my_form = LoginForm(request.form)
    if request.method == 'POST':
        if my_form.validate():
            user = User(my_form.username.data, my_form.password.data);
            if user.is_existed() == 1:
                return 'Login success!'
            else:
                flash('Wrong username or password!')
                return render_template('login.html', form=my_form)
        else:
            flash('Please input username and password!')
            return render_template('login.html', form=my_form)
    return render_template('login.html', form=my_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    my_form = LoginForm(request.form)
    if request.method == 'POST':
        if my_form.validate():
            user = User(my_form.username.data, my_form.password.data)
            user.add()
            return 'Register success!'
        else:
            flash('Please input username and password!')
            return render_template('register.html', form=my_form)
    return render_template('register.html', form=my_form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        sum = int(num1) + int(num2)
        return render_template('add.html', sum=str(sum))
    return render_template('add.html')


class EntryForm(Form):
    sender = StringField('sender')
    content = TextAreaField('content', [validators.DataRequired()])


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    entry_list = get_all_entry()
    form = EntryForm(request.form)
    if request.method == 'POST':
        if form.validate():
            entry = Entry(form.sender.data, form.content.data)
            entry.add()
            entry_list = get_all_entry()
            return render_template('feedback.html', list=entry_list, form=form)
        else:
            flash('Please input content')
            return render_template('feedback.html', list=entry_list, form=form)
    return render_template('feedback.html', list=entry_list, form=form)


users = {
    'Tom': ['123456']
}


def gen_token(uid):
    token = base64.b64encode(':'.join([str(uid), str(random.random()), str(time.time() + 7200)]))
    users[uid].append(token)
    return token


def verify_token(token):
    _token = base64.b64decode(token)
    if not users.get(_token.split(':')[0])[-1] == token:
        return -1
    if float(_token.split(':')[-1]) >= time.time():
        return 1
    else:
        return 0


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    uid, pw = base64.b64decode(request.headers['Authorization'].split(' ')[-1]).split(':')
    if users.get(uid)[0] == pw:
        return gen_token(uid)
    else:
        return 'error'


@app.route('/test1', methods=['POST', 'GET'])
def test():
    token = request.args.get('token')
    if verify_token(token) == 1:
        return 'data'
    else:
        return 'error'


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
