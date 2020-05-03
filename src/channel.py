from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
from json import dumps, loads
from collections import defaultdict 
from blinker import signal
from sys import argv
from hashlib import sha256

from time import sleep


class Channel:

    def __init__(self, host, port, password):
        super().__init__()
        self.__message_table = defaultdict(bool)
        self.__data_table = defaultdict(bool)
        self.__lock = Lock()
        self.data_received = signal('data received')

        self.__sending_socket = socket(AF_INET, SOCK_STREAM)
        self.__receiving_socket = socket(AF_INET, SOCK_STREAM)
        self.__sending_socket.connect((host, int(port)))
        self.__receiving_socket.connect((host, int(port)))

        self.__sending_socket.sendall(sha256(password.encode()).digest())
        answer = self.__receiving_socket.recv(1024).decode()

        if answer.strip() == "GRANTED":
            print('Granted')
        else: 
            print('rejected')

    def __handle_awnser(self):
        while True:
            data = self.__receiving_socket.recv(4096).decode()
            if not data:
                break
            else:
                try:
                    self.__lock.acquire()
                    self.__data_table = defaultdict(bool, loads(data))
                    for key, value in self.__data_table.items():
                        self.__message_table[key] = value
                    self.__receiving_socket.sendall(b'Done.')
                    self.data_received.send(self)
                    self.__lock.release()
                except Exception as e:
                    print('Exception happened in handleing: ', e)

    def __send_message(self):
        self.__sending_socket.sendall(dumps(self.__message_table).encode())

    def start(self):
        self.awnser_thread = Thread(target=self.__handle_awnser)
        self.awnser_thread.start()

    def deactivate(self):
        self.__sending_socket.close()
        self.awnser_thread.join()

    def set_value(self, key, value):
        self.__lock.acquire()
        self.__message_table[key] = value
        self.__send_message()
        self.__lock.release()

    def set_values(self, keys, values):
        self.__lock.acquire()
        for index, key in keys.enumerate():
            self.__message_table[key] = values[index]
        self.__send_message()
        self.__lock.release()

    def get_value(self, key):
        self.__lock.acquire()
        data = self.__data_table[key]
        self.__lock.release()
        return data

    def get_values(self, keys):
        self.__lock.acquire()
        data = [ self.__data_table[key] if key in self.__data_table else False for key in keys ]
        self.__lock.release()
        return data


if __name__ == "__main__":
    Channel(argv[1], argv[2]).start()
    # TODO: