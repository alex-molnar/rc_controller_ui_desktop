from PyQt5.QtWidgets import QApplication
from main_window_qt import MainWindow
from sys import argv, exit


if __name__ == "__main__":

    app = QApplication(argv)
    app.setStyleSheet('''
        MainWindow {
            background-color: #b8e5ff;
        }
        
        ConnectDialog {
            background-color: #b8e5ff;
        }

        QPushButton, QLabel{
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            font-size: 25px;
            text-align: center;
        }
        
        QPushButton[dial="true"] {
            font-size: 18px;
        }

        QPushButton[active="true"] {
            background-color: yellow;
        }
        
        QPushButton#lights[active="true"] {
            background-color: #fdff82;
        }

        QLabel#linefollower {
            border: none;
        }
        
        QLabel[dial="true"] {
            font-size: 14px;
            border: none;
            background-color: #b8e5ff;
        }

        QLabel[active="true"] {
            border: 2px solid red;
        }

        QLabel[warning="true"] {
            background-color: yellow;
        }
        
        QLabel[collide="true"] {
            background-color: red;
        }

        QLabel#linefollower[active="true"] {
            background-color: black;
        }
        
        QLineEdit {
            background-color: #b8e5ff;
            border: none;
        }
    ''')

    window = MainWindow()
    window.resize(500, 500)
    window.show()

    exit(app.exec_())
