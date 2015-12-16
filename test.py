import requests

r = requests.get('http://127.0.0.1:5000/login1', auth=('Tom', '123456'))

token = r.text
print(token)

r = requests.get('http://127.0.0.1:5000/test1', params={'token': token})
print r.text
