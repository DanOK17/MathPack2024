import requests

name = input('Введите имя: ')
while True:
    text = input('Введите сообщение: ')
    response = requests.post('http://192.168.1.66:5000/send',
                             json={
                                 'name': name,
                                 'text': text
                             }
                            )
