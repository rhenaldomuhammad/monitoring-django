import time
import os
from datetime import datetime
import requests

TOKEN = '6250732185:AAEWwfi3B0uerfQu7n1dc4qyVjXy8biqnyA'
CHAT_ID = '1041111909'
LOG_FILE = '/var/log/apache2/error.log'
LAST_READ_POSITION_FILE = 'last_read_position.txt'
LAST_NOTIFICATION_TIME_FILE = 'last_notification_time.txt'
NOTIFICATION_INTERVAL = 120  # 2 minutes

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot6250732185:AAEWwfi3B0uerfQu7n1dc4qyVjXy8biqnyA/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_last_read_position():
    if not os.path.exists(LAST_READ_POSITION_FILE):
        with open(LAST_READ_POSITION_FILE, 'w') as file:
            file.write('0')
    with open(LAST_READ_POSITION_FILE, 'r') as file:
        position = file.read().strip()
        return int(position) if position.isdigit() else 0

def update_last_read_position(position):
    with open(LAST_READ_POSITION_FILE, 'w') as file:
        file.write(str(position))

def get_last_notification_time():
    if not os.path.exists(LAST_NOTIFICATION_TIME_FILE):
        with open(LAST_NOTIFICATION_TIME_FILE, 'w') as file:
            file.write(datetime.min.isoformat())
    with open(LAST_NOTIFICATION_TIME_FILE, 'r') as file:
        return datetime.fromisoformat(file.read().strip())

def update_last_notification_time():
    with open(LAST_NOTIFICATION_TIME_FILE, 'w') as file:
        file.write(datetime.now().isoformat())

def main():
    while True:
        last_read_position = get_last_read_position()
        last_notification_time = get_last_notification_time()

        with open(LOG_FILE, 'r') as file:
            file.seek(last_read_position)
            lines = file.readlines()
            update_last_read_position(file.tell())

        for line in lines:
            attack_detected = None
            if 'Remote Command Execution: Unix Command Injection' in line:
                attack_detected = 'Command Injection Attack'
            elif 'XSS Attack Detected via libinjection' in line:
                attack_detected = 'Cross-Site Scripting (XSS) Attack'
            elif 'SQL Injection Attack Detected via libinjection' in line:
                attack_detected = 'SQL Injection Attack'

            if attack_detected and (datetime.now() - last_notification_time).total_seconds() > NOTIFICATION_INTERVAL:
                send_telegram_message(f'{attack_detected} detected: ' + line)
                update_last_notification_time()
        time.sleep(10)  # Check the log every 10 seconds

if __name__ == '__main__':
    main()