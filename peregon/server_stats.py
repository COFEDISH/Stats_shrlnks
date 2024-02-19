import string
import socket
import json
import datetime

subd_address = ("cofesubd-service.default.svc.cluster.local", 6379)
server_address = ('0.0.0.0', 5003)
def format_time_interval(time_string):
    hours, minutes, seconds = time_string.split(':')
    start_time = f"{hours}:{minutes}"
    end_time = f"{hours}:{int(minutes) + 1:02}"
    return f"{start_time}-{end_time}"

def edit_data(json_data, link, ip, interval):
    data = json.loads(json_data)

    new_entry = {
        'URL': link,
        'IP': ip,
        'Time': interval
    }
    data.append(new_entry)
    return json.dumps(data)

def receive_data(data):

        if data:
            ip_address = data.get('ip_address')
            timestamp = data.get('timestamp')
            original_link = data.get('original_link')
            short_link = data.get('short_link')
            URL = original_link + f"({short_link})"
            if timestamp:
                date, time = timestamp.split('T')  # Разделяем дату и время по символу 'T'
                time_interval = format_time_interval(time)


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(subd_address)
                s.sendall(f"das78d78asd --file data{date}.json --query 'GSON get'".encode())
                print("Message sent successfully.")
                # Ожидание ответа от сервера
                datas_subd = s.recv(16384)
                data_sub = datas_subd.decode()
                print(data_sub)
            except ConnectionRefusedError:
                print("Connection to the server failed.")

        # Далее обрабатываем полученные данные
        data_subs = json.dumps(data_sub)  # Преобразование списка в строку JSON
        data_subd = json.loads(data_subs)  # Преобразование строки JSON в объект JSON
        new_data = edit_data(data_subd, URL, ip_address, time_interval)
        sended_data = json.loads(json.dumps(new_data))
        print(sended_data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subd:
            try:
                subd.connect(subd_address)
                subd.sendall(f"ds7fdsd87fdsf78 --file data{date}.json --query 'GSON save {sended_data}'".encode())
                print("Message sent successfully.")

                # Ожидание ответа от сервера
                response_from_subd = subd.recv(16384)
                print(response_from_subd)


            except ConnectionRefusedError:
                print("Connection to the server failed.")

def handle_connection():
    print("WebSocket connected!")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
        serv.bind(server_address)
        serv.listen()

        print("Waiting for connection...")
        conn, addr = serv.accept()
        print(f"Connection from {addr}")
        datas = conn.recv(1024)
        data = json.loads(datas.decode())

    if data:
        receive_data(data)



if __name__ == '__main__':
    while True:
        handle_connection()


