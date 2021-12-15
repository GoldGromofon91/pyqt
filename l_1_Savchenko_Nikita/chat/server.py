import select
import CONFIGS
from socket import socket, AF_INET, SOCK_STREAM

from function import create_ip_port, request_server, get_message_from_server, check_message_on_server, send


def start_server():
    ip,port = create_ip_port(type='client')
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind((ip, port))
    listen_socket.listen(CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('MAX_CONNECTIONS'))
    listen_socket.settimeout(0.3)

    client_list = []

    while True:
        try:
            client, addr = listen_socket.accept()
            client_list.append(client)
        except OSError:
            pass

        read_clients, write_clients, error,user_messages = [],[],[],[]

        try:
            read_clients, write_clients, error = select.select(client_list, client_list, [], 0)
        except:
            pass

        if read_clients:
            for read_user_socket in read_clients:
                message = get_message_from_server(read_user_socket)

                if message['action'] == 'presence':
                    response = check_message_on_server(message)
                    try:
                        send(read_user_socket, response)
                    except:
                        read_clients.remove(read_user_socket)
                        pass

                if message['action'] == 'msg':
                    user_messages.append(message)

        if user_messages and write_clients:
            for message in user_messages:
                for waiting_user in write_clients:
                    send(waiting_user, message)
                user_messages.remove(message)


if __name__ == "__main__":
    start_server()
