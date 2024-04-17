# This is the third homework assignment

To install the required libraries, enter the command:
`pip install -r requirements.txt`

## How to run the application

1. Run the server: `python server.py`
2. Run the sender: `python sender.py`
3. Run the receiver: `python receiver.py`

## How to use

### Sender

1. Enter your name when prompted.
2. Type a message and hit Enter to send it.

### Receiver

The receiver will print out all incoming messages with the timestamp and sender's name.

### Commands

The server supports the following commands:

- `\help` - Shows the list of available commands.
- `\weather` - Gets a mock weather forecast.
- `\lastname [value]` - Set your last name.
- `\address [street address], [city], [postal code]` - Set your address.
- `\phone [value]` - Add a phone number.
- `\color [color]` - Set the color of the output text.

### Status

You can check the server status by visiting `http://192.168.1.66:5000/status` in your browser. It will show the number of users, total messages sent, and your personal information (last name, address, and phone numbers) set using the commands.