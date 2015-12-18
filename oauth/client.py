# coding=utf-8

from flask import Flask, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth

CLIENT_ID = '9Msq8P6xAM7ozigbwM4kqpdVm28Qb15HbpPFZ0fC'
CLIENT_SECRET = 'Aw7fOVZv48uXZBaLHuxdYbU0RDrKXYwF3dmUltIL4A4NUXm3IE'

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
oauth = OAuth(app)

remote = oauth.remote_app(
        'remote',
        consumer_key=CLIENT_ID,
        consumer_secret=CLIENT_SECRET,
        request_token_params={'scope': 'email'},
        base_url='http://127.0.0.1:5000/api/',
        request_token_url=None,
        access_token_url='http://127.0.0.1:5000/oauth/token',
        authorize_url='http://127.0.0.1:5000/oauth/authorize'
)


# 用于重定向用户登录
@app.route('/')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        return jsonify(resp.data)
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
            callback=url_for('authorized', next=next_url, _external=True))


# 用于获取token，并存储在session中
@app.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    print resp
    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')


if __name__ == '__main__':
    import os

    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(port=8000, debug=True)
