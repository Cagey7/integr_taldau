import requests

url = 'http://5.63.114.131:8000/api/v1/loader/insert-all-indices/'

token = '49fbafd7abda1ea11437ba307fc15e13edeae6bc'

headers = {'Authorization': 'Token ' + token}

x = requests.post(url, headers=headers)

print(x.text)