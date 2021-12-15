from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from function import get_presence_message, send, get_message_from_server, check_message_on_client, create_ip_port, \
    sender_msg, writer_msg



def start():
    #Получаем ip,port
    ip,port = create_ip_port(type='client')
    # Открываем сокет
    new_socket = socket(AF_INET,SOCK_STREAM)
    new_socket.connect((ip,port))
    user_name = input('Enter username: ')
    message = get_presence_message(user_name)
    send(new_socket,message)

    # Получаем ответ от сервера
    response = get_message_from_server(new_socket)
    output = check_message_on_client(response)

    if output:
        print(f'You are in chat, status - {output["status"]}')

    else:
        raise Exception('Error connect')

    sender = Thread(target=sender_msg, kwargs={'transport': new_socket, 'account_name': user_name})
    sender.start()

    writer = Thread(target=writer_msg, kwargs={'transport': new_socket})
    writer.start()

if __name__ == "__main__":
    start()
