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
        self.pbInsert.clicked.connect(self.insert_student)
        self.pbDelete.clicked.connect(self.delete_student)
        self.pbFind.clicked.connect(self.find_for_val)

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

     def update_twStudents(self, query="select * from students"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStudents.setRowCount(0)
        for i, row in enumerate(data):
            self.twStudents.setRowCount(self.twStudents.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStudents.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStudents.resizeColumnsToContents()

    def insert_student(self):
        row = [self.leFio.text(), 'муж' if self.rbMale.isChecked() else 'жен', self.sbAge.text(),
               self.lePhone.text(), self.leEmail.text(), self.leGroup.text(),
               self.sbCurs.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into students(fio, sex, age, phone, email, `group`, curs)
            values('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}', {row[6]})""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStudents()

    def delete_student(self):
        row = self.twStudents.currentRow()
        num = self.twStudents.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from students where num = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStudents()

    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStudents(f"select * from students where `{col}` like '{val}%'")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())