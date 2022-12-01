import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from main_form import Ui_MainWindow

# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())