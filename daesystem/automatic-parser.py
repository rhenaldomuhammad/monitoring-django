#final code rev
from datetime import datetime
import re
import mysql.connector

# ambil file
log_file_path = '/var/log/apache2/error.log'

# koneksi db
db_config = {
    'host': 'localhost',
    'user': 'auditer1',
    'password': 'auditer!',
    'database': 'modsecurity_parser'
}

# parser log ke db
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    with open(log_file_path, 'r') as file:
        for line in file:
            # Ekspresi reguler diperbarui untuk mengekstrak jenis serangan
            match = re.search(r'\[([A-Za-z]{3} \w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6} \d{4})\].*\[client (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\].*\[id "\d+"\] \[msg "(.*?)"\]', line)
            if match:
                timestamp_str, client_ip, message = match.groups()
                attack_type = None

                # Identifikasi jenis serangan berdasarkan pesan
                if "Remote Command Execution: Unix Command Injection" in message:
                    attack_type = "Unix Command Injection"
                elif "XSS Attack Detected via libinjection" in message:
                    attack_type = "XSS Attack"
                elif "SQL Injection Attack Detected via libinjection" in message:
                    attack_type = "SQL Injection"

                # Jika jenis serangan dikenal, lakukan penyimpanan ke dalam database
                if attack_type:
                    # Konversi format timestamp
                    log_timestamp = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S.%f %Y')
                    mysql_timestamp = log_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                    # Simpan semua informasi yang diinginkan ke database
                    insert_query = "INSERT INTO logs1 (timestamp, client_ip, attack_type, message) VALUES (%s, %s, %s, %s)"
                    values = (mysql_timestamp, client_ip, attack_type, message)
                    cursor.execute(insert_query, values)

    connection.commit()
    print("Parser Log Berhasil.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection is Closed.")
