import pymysql
import re
import time
from datetime import datetime

# Konfigurasi database
DB_HOST = 'localhost'
DB_USER = 'adminer1'
DB_PASSWORD = 'adminer!'
DB_NAME = 'log_parser'
LOG_FILE_PATH = '/var/log/apache2/error.log'

# Fungsi untuk menghubungkan ke database
def connect_to_database():
    return pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# Fungsi untuk mendapatkan timestamp terakhir yang diproses
def get_last_processed_timestamp(cursor):
    query = "SELECT MAX(timestamp) FROM log_table"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result and result[0] else datetime.min

# Fungsi untuk memproses log
def process_logs():
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    last_processed_timestamp = get_last_processed_timestamp(cursor)

    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            match = re.search(r'\[([A-Za-z]{3} \w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6} \d{4})\].*\[client (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\].*\[msg "(.*?)"\]', line)
            if match:
                timestamp_str, client_ip, message = match.groups()

                # Konversi format timestamp
                log_timestamp = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S.%f %Y')
                mysql_timestamp = log_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                if log_timestamp > last_processed_timestamp and (
                    "Remote Command Execution: Unix Command Injection" in message or
                    "XSS Attack Detected via libinjection" in message or
                    "SQL Injection Attack Detected via libinjection" in message
                ):
                    insert_query = "INSERT INTO log_table (timestamp, client_ip, message) VALUES (%s, %s, %s)"
                    values = (mysql_timestamp, client_ip, message)
                    cursor.execute(insert_query, values)
                    db_connection.commit()

    cursor.close()
    db_connection.close()

# Fungsi utama untuk menjalankan daemon
def main():
    while True:
        process_logs()
        time.sleep(3600)  # Tunggu selama 1 jam (3600 detik)

if __name__ == "__main__":
    main()
