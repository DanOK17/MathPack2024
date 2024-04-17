from datetime import datetime
from time import sleep

import requests

def print_message(message):
    t = message['time']
    dt = datetime.fromtimestamp(t)
    print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} {message['name']}: {message['text']}")

after = 0
while True:
    response = requests.get(
        'http://192.168.1.66:5000/messages',                                                      #'http://127.0.0.1:5000/messages',
                            params={'after': after})
    messages = response.json()['messages']
    if len(messages) > 0:
        for message in messages:
            print_message(message)
        after = message['time']
    sleep(1)
