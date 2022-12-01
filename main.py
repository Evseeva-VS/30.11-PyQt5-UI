import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from main_form import Ui_MainWindow

# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.rbMale.setChecked(True)
        self.pbOpen.clicked.connect(self.open_file)

    def open_file(self):
        try:
            self.conn = sqlite3.connect('students_db.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from students")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStudents.setColumnCount(len(col_name))
        self.twStudents.setHorizontalHeaderLabels(col_name)
        self.twStudents.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStudents.setRowCount(self.twStudents.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStudents.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStudents.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())