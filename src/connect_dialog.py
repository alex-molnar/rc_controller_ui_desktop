from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt5.Qt import Qt


class ConnectDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(150, 200)

        self.host_label = QLabel('Host: ', self)
        self.port_label = QLabel('Port: ', self)
        self.password_label = QLabel('Password: ', self)
        for label in [self.host_label, self.port_label, self.password_label]:
            label.resize(69, 30)
            label.setAlignment(Qt.AlignCenter)
            label.setProperty('dial', True)

        self.host_label.move(3, 10)
        self.port_label.move(3, 60)
        self.password_label.move(3, 110)

        self.host_field = QLineEdit(self)
        self.port_field = QLineEdit(self)
        self.password_field = QLineEdit(self)
        for label in [self.host_field, self.port_field, self.password_field]:
            label.resize(69, 30)
            label.setAlignment(Qt.AlignCenter)
        self.host_field.move(78, 10)
        self.port_field.move(78, 60)
        self.password_field.move(78, 110)
        self.password_field.setEchoMode(QLineEdit.Password)

        self.connect_button = QPushButton(self)
        self.connect_button.setText('Connect')
        self.connect_button.resize(100, 30)
        self.connect_button.move(25, 160)
        self.connect_button.setProperty('dial', True)
        self.connect_button.clicked.connect(self.accept)
