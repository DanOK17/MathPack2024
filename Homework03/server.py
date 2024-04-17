# save this as app.py
import flask
from flask import Flask, abort, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pydantic import BaseModel, Field, validator
import time
import requests
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = []
user_colors = {}
DbNameList = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': 12345,
        'text': 'text01923097'
    })

user_info = {
    'lastName': '',
    'address': {
        'streetAddress': '',
        'city': '',
        'postalCode': ''
    },
    'phoneNumbers': []
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("start.html")

class MessageModel(BaseModel):
    name: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)

    @validator('name', 'text')
    def validate_strings(cls, value):
        if not isinstance(value, str):
            raise ValueError('Name and text should be strings')
        return value

    class Config:
        anystr_strip_whitespace = True

def process_command(message):
    global user_info
    command, *args = message.text.split(' ', 1)
    if command == '\\help':
        return "Commands:\n\\lastname [value] - set last name\n\\address [value] - set address\n\\phone [value] - add phone number\n\\weather - get current weather\n\\color [value] - set text color"
    elif command == '\\lastname':
        if args:
            user_info['lastName'] = args[0]
            return f"Last name set to: {user_info['lastName']}"
        else:
            return "Usage: \\lastname [value]"
    elif command == '\\address':
        if args:
            address_parts = args[0].split(',')
            if len(address_parts) == 3:
                user_info['address']['streetAddress'] = address_parts[0].strip()
                user_info['address']['city'] = address_parts[1].strip()
                user_info['address']['postalCode'] = address_parts[2].strip()
                return "Address set successfully"
            else:
                return "Invalid address format. Use: \\address [street address], [city], [postal code]"
        else:
            return "Usage: \\address [street address], [city], [postal code]"
    elif command == '\\phone':
        if args:
            phone_number = args[0]
            user_info['phoneNumbers'].append(phone_number)
            return f"Phone number {phone_number} added successfully"
        else:
            return "Usage: \\phone [value]"
    elif command == '\\weather':
        if 'city' in user_info['address'] and user_info['address']['city']:
            city = user_info['address']['city']
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8537d9ef6386cb97156fd47d832f479c&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['description']
                temperature = data['main']['temp']
                return f"Current weather in {city}: {weather}, Temperature: {temperature}°C"
            else:
                return "Failed to retrieve weather data"
        else:
            return "Address not set. Please set your address first using \\address command"
    elif command == '\\color':
        if args:
            color = args[0]
            user_colors[message.name] = color
            return f"Text color set to: {color}"
        else:
            return "Usage: \\color [value]"
    else:
        return f"Unknown command: {command}"

@app.route("/send", methods=['POST'])
def send_message():
    try:
        data = MessageModel(**flask.request.form)
    except ValueError as e:
        return {'error': str(e)}, 400

    file = flask.request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_url = filename
    else:
        file_url = None

    if data.text.startswith('\\'):
        response = process_command(data)
        message = {
            'text': response,
            'name': data.name,
            'time': time.time(),
            'color': user_colors.get(data.name, 'black'),
            'file': file_url
        }
    else:
        message = {
            'text': data.text,
            'name': data.name,
            'time': time.time(),
            'color': user_colors.get(data.name, 'black'),
            'file': file_url
        }

    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    users = list(set([message['name'] for message in db]))
    num_users = len(users)
    num_messages = len(db)

    if len(db) > 0:
        latest_message = db[-1]
        name = latest_message['name'].split(' ', 1)
        if len(name) > 1:
            firstName, lastName = name
        else:
            firstName, lastName = name[0], user_info['lastName']
    else:
        firstName, lastName = 'Anonymous', user_info['lastName']

    return flask.render_template('status.html', firstName=firstName, lastName=lastName,
                                  address=user_info['address'],
                                  phoneNumbers=user_info['phoneNumbers'],
                                  numUsers=num_users, numMessages=num_messages, users=users,
                                  root_url=flask.url_for('index'))

@app.route('/index')
def lionel():
    return flask.render_template('index.html')

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(host='192.168.1.66', port=5000)