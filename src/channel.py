from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
from json import dumps, loads
from collections import defaultdict
from hashlib import sha256


class Channel:

    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'turn_left'
    RIGHT = 'turn_right'
    R_INDICATOR = 'right_indicator'
    L_INDICATOR = 'left_indicator'
    HAZARD_WARNING = 'hazard_warning'
    LIGHTS = 'lights'
    HORN = 'horn'
    DISTANCE = 'distance'
    SPEED = 'speed'
    LINE = 'line'
    REVERSE = 'reverse'

    DISTANCE_KEEPING = 'distance_keeping'
    LINE_FOLLOWING = 'line_following'

    CHANGE_DIRECTION = 'change_direction'  # TODO: constants anyway

    def __init__(self, host, port, password):
        super().__init__()
        self.__message_table = defaultdict(bool)
        self.__data_table = defaultdict(bool)
        self.__lock = Lock()

        self.__sending_socket = socket(AF_INET, SOCK_STREAM)
        self.__receiving_socket = socket(AF_INET, SOCK_STREAM)
        self.__sending_socket.connect((host, int(port)))
        self.__receiving_socket.connect((host, int(port)))

        self.__sending_socket.sendall(sha256(password.encode()).digest())
        answer = self.__receiving_socket.recv(1024).decode()

        if answer.strip() == "GRANTED":
            print('Granted')
            self.answer_thread = Thread(target=self.__handle_awnser)
            self.answer_thread.start()
        else:
            print('rejected')

    def __handle_awnser(self):
        while True:
            data = self.__receiving_socket.recv(1024).decode().strip()
            if not data:
                break
            else:
                try:
                    self.__lock.acquire()
                    self.__data_table = defaultdict(bool, loads(data))
                    for key, value in self.__data_table.items():
                        self.__message_table[key] = value
                    self.__receiving_socket.sendall(b'Done.')
                    self.__lock.release()
                except Exception as e:
                    print('Exception happened in handleing: ', e)

    def __send_message(self):
        self.__sending_socket.sendall(dumps(self.__message_table).encode())

    def deactivate(self):
        self.__sending_socket.close()
        self.answer_thread.join()

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
        data = [self.__data_table[key] if key in self.__data_table else False for key in keys]
        self.__lock.release()
        return data
