import requests

# r = requests.get('http://127.0.0.1:5000/login1', auth=('Tom', '123456'))
#
# token = r.text
# print(token)
#
# r = requests.get('http://127.0.0.1:5000/test1', params={'token': token})
# print r.text

r = requests.get('http://127.0.0.1:5000/client/login')
print(r.text)
print(r.url)
uri_login = r.url.split('?')[0] + '?user=Tom&pw=123456'
r = requests.get(uri_login)
print(r.text)
