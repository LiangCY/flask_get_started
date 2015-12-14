from flask import Flask, request, url_for, render_template
from models import User

app = Flask(__name__)


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
    user = None
    if int(id) == 1:
        user = User(1, 'lcy')
    return render_template('user_id.html', user=user)


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


if __name__ == '__main__':
    app.run()
