import sys
import socket
import time
from utils.moduls import Proto
from services import actions
from socket import *
import json
import logging.config
from threading import Thread
from utils.descriptors import HostPortDescriptor
from utils.metaclass import DocMeta
from client_db import ClientDatabase
import os
import sys
from client.main_window import ClientMainWindow
from PyQt5.QtWidgets import QApplication


class Client(Thread, Proto, metaclass=DocMeta):
    listen_ip = HostPortDescriptor()
    listen_port = HostPortDescriptor()

    def __init__(self, database, transport, account_name):

        self.database = database
        self.transport = transport
        self.account_name = 'artem trubin'

        # НАСТРОЙКИ ЛОГИРОВАНИЯ
        logging.config.fileConfig('log/logging.ini',
                                  disable_existing_loggers=False,
                                  defaults={'logfilename': 'log/client.log'})
        self.logger = logging.getLogger('client')

        # ЗАГРУЖАЮ НАСТРОЙКИ
        self.config = self.load_settings()

        # БЕРУ ПОРТ И IP
        try:
            self.listen_ip = sys.argv[1]
        except IndexError:
            self.logger.error(f'listen_ip клиента передан не верно. '
                              f'Были использованы аргументы из файла settings.ini')
            self.listen_ip = self.config['DEFAULT_IP_ADDRESS']

        try:
            self.listen_port = sys.argv[2]
        except IndexError:
            self.logger.error(f'listen_port клиента передан не верно. '
                              f'Были использованы аргументы из файла settings.ini')
            self.listen_port = int(self.config['DEFAULT_PORT'])

        # Конструктор предка
        super(Client, self).__init__()

    def create_presence_message(self, account_name):
        """:создание PRESENCE СООБЩЕНИЯ
         """
        message = {
            self.config['ACTION']: actions.PRESENCE,
            self.config['TIME']: time.ctime(time.time()),
            self.config['USER']: {
                self.config['ACCOUNT_NAME']: account_name
            }
        }
        self.logger.info(f'Сформировано presence сообщение')
        return message

    def create_msg(self, message, account_name):
        """:создание обычного СООБЩЕНИЯ
           """
        message_to_send = {
            self.config['ACTION']: actions.MSQ,
            self.config['TIME']: time.ctime(time.time()),
            self.config['TO']: "#room_name",
            self.config['FROM']: account_name,
            self.config['MESSAGE']: message
        }
        self.logger.info(f'Сформировано msg от клиента')
        self.database.save_message(account_name, message_to_send['to'], message)
        return message_to_send

    def check_responce(self, responce):
        """:проверка ответа от сервера
        """
        if self.config['RESPONSE'] in responce:
            if responce[self.config['RESPONSE']] == 200:
                self.logger.info(f'От сервера пришел ответ - 200')
                return '200'
            if responce[self.config['RESPONSE']] == 400:
                self.logger.error(f'От сервера пришел ответ - 400 \n'
                                  f'{responce}')
                return '400'
        raise ValueError

    def thread_for_send(self, transport, account_name):
        """:создание потока для отправки сообщений
        """
        while True:
            message = input('Введите сообщение: ')
            msg = self.create_msg(message, account_name)
            self.send_message(transport, msg, self.config['ENCODING'])
            self.logger.info(f'Отправлено сообщение серверу {msg["message"]}')

    def thread_for_write(self, transport):
        """:создание потока для чтения сообщений
        """
        while True:
            msg = self.get_message(transport, int(self.config['MAX_PACKAGE_LENGTH']), self.config['ENCODING'])
            self.logger.info(f'Получено сообщение от {msg["from"]} - {msg["message"]}')
            print(msg['message'])

    def run(self):
        """:запуск клиента
        """
        self.transport.connect((self.listen_ip, self.listen_port))

        self.logger.info(f'Успешное подключение на клиенте: host {self.listen_ip}, port {self.listen_port}')

        presence_message = self.create_presence_message(self.account_name)
        self.send_message(self.transport, presence_message, self.config['ENCODING'])
        self.logger.info(f'Сообщение от клиента отправлено успешно')

        try:
            response = self.get_message(self.transport, int(self.config['MAX_PACKAGE_LENGTH']), self.config['ENCODING'])
            check = self.check_responce(response)
            self.logger.info(f'Соединение с сервером успешно установлено: ответ {check}')
        except (ValueError, json.JSONDecodeError):
            self.logger.error(f'Ошибка декодирования сообщения', exc_info=True)

        send = Thread(target=self.thread_for_send,
                      kwargs={'transport': self.transport, 'account_name': self.account_name})
        send.start()

        write = Thread(target=self.thread_for_write, kwargs={'transport': self.transport})
        write.start()


def start_client_with_gui():
    account_name = 'artem trubin'
    transport = socket(AF_INET, SOCK_STREAM)
    name = os.path.basename(sys.argv[0]).split('.')[0]
    database = ClientDatabase(name)
    client = Client(database, transport, account_name)
    client.daemon = True
    client.start()

    # Создаём GUI
    client_app = QApplication(sys.argv)
    main_window = ClientMainWindow(database, client)
    main_window.setWindowTitle(f'Чат Программа alpha release - {name}')
    client_app.exec_()


if __name__ == '__main__':
    start_client_with_gui()
