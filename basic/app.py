# coding=utf-8

from flask import Flask, request, url_for, render_template, flash, redirect, abort, make_response

from model import *

from wtforms import Form, StringField, PasswordField, validators, TextAreaField

import base64
import random
import time
import hmac
import json
from datetime import datetime, timedelta

from flask_restful import Resource, Api, fields, marshal_with

app = Flask(__name__)
app.secret_key = '123456'
api = Api(app)


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
            user = User(my_form.username.data, my_form.password.data)
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

auth_code = {}
redirect_uri = 'http://127.0.0.1:5000/client/passport'
client_id = '123456'
users[client_id] = []
oauth_redirect_uri = []

TIMEOUT = 3600 * 2


# 生成授权码
def gen_code(uri, user_id):
    code = random.randint(0, 10000)
    auth_code[uri] = [code, user_id]
    return code


# 生成签名
def get_signature(value):
    return hmac.new('secret', value).digest()


def encode_token_bytes(data):
    return base64.urlsafe_b64encode(data)


def decode_token_bytes(data):
    return base64.urlsafe_b64decode(data)


def gen_token(data):
    data = data.copy()
    if "salt" not in data:
        data['salt'] = unicode(random.random()).decode('ascii')
    if 'expires' not in data:
        data['expires'] = time.time() + TIMEOUT
    payload = json.dumps(data).encode('utf8')
    sig = get_signature(payload)
    return encode_token_bytes(payload + sig)


def verify_token(token):
    decoded_token = decode_token_bytes(str(token))
    payload = decoded_token[:-16]
    sig = decoded_token[-16:]
    expected_sig = get_signature(payload)
    if sig != expected_sig:
        return {}
    data = json.loads(payload.decode('utf8'))
    if data.get('expires') >= time.time():
        return data
    return 0


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    uid, pw = base64.b64decode(request.headers['Authorization'].split(' ')[-1]).split(':')
    if users.get(uid)[0] == pw:
        return gen_token(uid)
    else:
        return 'error'


@app.route('/client/login', methods=['POST', 'GET'])
def client_login():
    uri = 'http://127.0.0.1:5000/oauth?response_type=code&client_id=%s&redirect_uri=%s' % (client_id, redirect_uri)
    return redirect(uri)


@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    if request.method == 'POST' and request.form['user']:
        u = request.form['user']
        p = request.form['pw']
        if users.get(u)[0] == p and oauth_redirect_uri:
            uri = oauth_redirect_uri[0] + '?code=%s' % gen_code(oauth_redirect_uri[0], u)
            expire_date = datetime.now() + timedelta(minutes=1)
            resp = make_response(redirect(uri))
            resp.set_cookie('login', '_'.join([u, p]), expires=expire_date)
            return resp
    if request.args.get('code'):
        auth_info = auth_code.get(request.args.get('redirect_uri'))
        if str(auth_info[0]) == request.args.get('code'):
            return gen_token(dict(client_id=request.args.get('client_id'), user_id=auth_info[1]))
    if request.args.get('redirect_uri'):
        oauth_redirect_uri.append(request.args.get('redirect_uri'))
        if request.cookies.get('login'):
            u, p = request.cookies.get('login').split('_')
            if users.get(u)[0] == p:
                uri = oauth_redirect_uri[0] + '?code=%s' % gen_code(oauth_redirect_uri[0], u)
                return redirect(uri)
        return '''
            <form method='post'>
                <p><input type='text' name='user'></p>
                <p><input type='password' name='pw'></p>
                <p><input type='submit' value='login'></p>
            </form>
        '''


@app.route('/client/passport', methods=['POST', 'GET'])
def passport():
    code = request.args.get('code')
    uri = 'http://127.0.0.1:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s' % (
        code, redirect_uri, client_id)
    return redirect(uri)


# 资源服务器
@app.route('/test', methods=['POST', 'GET'])
def test():
    token = request.args.get('token')
    ret = verify_token(token)
    if ret:
        return json.dumps(ret)
    else:
        return 'error'


# marshal
resource_fields = {
    'user': fields.String(attribute='sender', default=''),
    'content': fields.String(default=''),
}


# 新的资源服务器
class Test1(Resource):
    @marshal_with(resource_fields)
    def get(self):
        token = request.args.get('token')
        ret = verify_token(token)
        if ret:
            return get_all_entry()
        else:
            return 'error'


api.add_resource(Test1, '/test1')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
