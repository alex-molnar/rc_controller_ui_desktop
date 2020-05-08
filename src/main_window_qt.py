from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import Qt
from threading import Thread, Lock
from src.channel import Channel
from src.connect_dialog import ConnectDialog

from time import sleep


class Button(QPushButton):
    def keyPressEvent(self, event):
        event.ignore()


class MainWindow(QWidget):

    DISTANCE_TEXT = 'Distance: '
    DISTANCE_MEASURE = 'cm'
    SPEED_TEXT = 'Speed: '
    SPEED_MEASURE = 'km/h'

    R_INDICATOR = 'right_indicator'
    L_INDICATOR = 'left_indicator'
    HAZARD_WARNING = 'hazard_warning'
    LIGHTS = 'lights'
    HORN = 'horn'
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'turn_left'
    RIGHT = 'turn_right'
    DISTANCE = 'distance'
    SPEED = 'speed'
    LINE = 'line'
    REVERSE = 'reverse'

    widget_update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        dial = ConnectDialog(self)
        dial.exec()

        # tmp!!!!! TODO:
        port = input('port: ')
        if port == '':
            port = 8000
        self.channel = Channel('192.168.1.11', int(port), '69420')
        # self.channel = Channel(dial.host_field.text(), dial.port_field.text(), dial.password_field.text())

        self.move_buttons = dict()
        self.light_buttons = dict()
        self.distance_label = None
        self.speed_label = None
        self.line_label = None

        self.place_move_buttons()
        self.place_light_buttons()
        self.place_labels()

        self.widget_update_signal.connect(self.update_widgets)
        self.lock = Lock()

        Thread(target=self.supervise_update).start()

    def place_move_buttons(self):
        self.move_buttons[self.FORWARD] = QLabel('🡅', self)
        self.move_buttons[self.BACKWARD] = QLabel('🡇', self)
        self.move_buttons[self.LEFT] = QLabel('🡄', self)
        self.move_buttons[self.RIGHT] = QLabel('🡆',self)
        self.move_buttons[self.REVERSE] = QLabel('R', self)

        for button in self.move_buttons.values():
            button.resize(100, 100)
            button.setAlignment(Qt.AlignCenter)
            button.setProperty('active', False)

        self.move_buttons[self.REVERSE].resize(50, 50)

        self.move_buttons[self.FORWARD].move(200, 250)
        self.move_buttons[self.BACKWARD].move(200, 350)
        self.move_buttons[self.LEFT].move(100, 350)
        self.move_buttons[self.RIGHT].move(300, 350)
        self.move_buttons[self.REVERSE].move(125, 275)

    def place_light_buttons(self):
        self.light_buttons[self.R_INDICATOR] = Button(self)
        self.light_buttons[self.R_INDICATOR].setGeometry(400, 50, 50, 50)
        self.light_buttons[self.R_INDICATOR].setText('🡂')

        self.light_buttons[self.L_INDICATOR] = Button(self)
        self.light_buttons[self.L_INDICATOR].setGeometry(50, 50, 50, 50)
        self.light_buttons[self.L_INDICATOR].setText('🡀')

        self.light_buttons[self.HAZARD_WARNING] = Button(self)
        self.light_buttons[self.HAZARD_WARNING].setGeometry(225, 80, 50, 50)
        self.light_buttons[self.HAZARD_WARNING].setText('⚠')

        self.light_buttons[self.LIGHTS] = Button(self)
        self.light_buttons[self.LIGHTS].setGeometry(225, 150, 50, 50)
        self.light_buttons[self.LIGHTS].setText('⛭')
        self.light_buttons[self.LIGHTS].setObjectName('lights')

        for light in self.light_buttons.values():
            light.setProperty('active', False)

    def place_labels(self):
        self.distance_label = QLabel(self.DISTANCE_TEXT + '0.0' + self.DISTANCE_MEASURE, self)
        self.speed_label = QLabel(self.SPEED_TEXT + '0.0' + self.SPEED_MEASURE, self)
        self.line_label = QLabel(parent=self)

        for label in [self.distance_label, self.speed_label]:
            label.resize(200, 50)
            label.setAlignment(Qt.AlignCenter)
            label.setProperty('warning', False)
            label.setProperty('collide', False)

        self.line_label.resize(20, 60)
        self.line_label.setObjectName('linefollower')
        self.line_label.setProperty('active', False)

        self.distance_label.move(15, 150)
        self.speed_label.move(285, 150)
        self.line_label.move(240, 10)

    def keyPressEvent(self, event): 
        if not event.isAutoRepeat():
            key = event.key()

            if key == Qt.Key_Q:
                self.channel.set_value(self.L_INDICATOR, not self.channel.get_value(self.L_INDICATOR))
            elif key == Qt.Key_E:
                self.channel.set_value(self.R_INDICATOR, not self.channel.get_value(self.R_INDICATOR))
            elif key == Qt.Key_H:
                self.channel.set_value(self.HAZARD_WARNING, not self.channel.get_value(self.HAZARD_WARNING))
            elif key == Qt.Key_L:
                self.channel.set_value(self.LIGHTS, not self.channel.get_value(self.LIGHTS))
            elif key == Qt.Key_R:
                self.channel.set_value(self.REVERSE, not self.channel.get_value(self.REVERSE))
            elif key == Qt.Key_B:
                self.channel.set_value(self.HORN, True)
            elif key in (Qt.Key_W, Qt.Key_Up):
                self.channel.set_value(self.FORWARD, True)
            elif key in (Qt.Key_S, Qt.Key_Down):
                self.channel.set_value(self.BACKWARD, True)
            elif key in (Qt.Key_A, Qt.Key_Left):
                self.channel.set_value(self.LEFT, True)
            elif key in (Qt.Key_D, Qt.Key_Right):
                self.channel.set_value(self.RIGHT, True)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if key == Qt.Key_B:
                self.channel.set_value(self.HORN, False)
            elif key in (Qt.Key_W, Qt.Key_Up):
                self.channel.set_value(self.FORWARD, False)
            elif key in (Qt.Key_S, Qt.Key_Down):
                self.channel.set_value(self.BACKWARD, False)
            elif key in (Qt.Key_A, Qt.Key_Left):
                self.channel.set_value(self.LEFT, False)
            elif key in (Qt.Key_D, Qt.Key_Right):
                self.channel.set_value(self.RIGHT, False)

    def update_widgets(self):
        self.lock.acquire(timeout=1)

        self.distance_label.setText(
            self.DISTANCE_TEXT + 
            str(self.channel.get_value(self.DISTANCE)) + 
            self.DISTANCE_MEASURE
        )

        old_value = self.distance_label.property('collide')
        self.distance_label.setProperty('collide', self.channel.get_value(self.DISTANCE) < 10)
        if old_value != self.distance_label.property('collide'):
            self.distance_label.setStyle(self.distance_label.style())
        else:
            old_value = self.distance_label.property('warning')
            self.distance_label.setProperty('warning', self.channel.get_value(self.DISTANCE) < 25)
            if old_value != self.distance_label.property('warning'):
                self.distance_label.setStyle(self.distance_label.style())

        self.speed_label.setText(
            self.SPEED_TEXT +
            str(self.channel.get_value(self.SPEED)) +
            self.SPEED_MEASURE
        )

        old_value = self.speed_label.property('collide')
        self.speed_label.setProperty('collide', self.channel.get_value(self.SPEED) > 30)
        if old_value != self.speed_label.property('collide'):
            self.speed_label.setStyle(self.speed_label.style())
        else:
            old_value = self.speed_label.property('warning')
            self.speed_label.setProperty('warning', self.channel.get_value(self.SPEED) > 20)
            if old_value != self.speed_label.property('warning'):
                self.speed_label.setStyle(self.speed_label.style())

        old_value = self.line_label.property('active')
        self.line_label.setProperty('active', self.channel.get_value(self.LINE))
        if old_value != self.line_label.property('active'):
            self.line_label.setStyle(self.line_label.style())

        for name, button in self.light_buttons.items():
            old_value = button.property('active')
            button.setProperty('active', self.channel.get_value(name))
            if old_value != button.property('active'):
                button.setStyle(button.style())

        for name, button in self.move_buttons.items():
            old_value = button.property('active')
            button.setProperty('active', self.channel.get_value(name))
            if old_value != button.property('active'):
                button.setStyle(button.style())

        self.lock.release()

    def closeEvent(self, event):
        self.channel.deactivate()
        self.lock.acquire()
        super().closeEvent(event)

    def supervise_update(self):
        while self.lock.acquire(timeout=1):
            self.lock.release()
            self.widget_update_signal.emit()
            sleep(0.05)
