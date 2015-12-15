# coding=utf-8

from flask import Flask, request, url_for, render_template, flash, abort

from models import User

from db import *

from wtforms import Form, StringField, PasswordField, validators

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
        if my_form.validate() and my_form.username.data == 'lcy' and my_form.password.data == '123456':
            flash('Login success!')
            return render_template('login.html', form=my_form)
        else:
            flash('Login failed!')
            return render_template('login.html', form=my_form)
    return render_template('login.html', form=my_form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        sum = int(num1) + int(num2)
        return render_template('add.html', sum=str(sum))
    return render_template('add.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
