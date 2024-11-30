import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.db = sqlite3.connect('coffee.sqlite')
        self.cur = self.db.cursor()
        self.loadTable()
        self.nextForm.clicked.connect(self.goToNextForm)

    def goToNextForm(self):
        self.next = AddCoffee(self)
        self.next.show()

    def update(self):
        self.tableWidget.clearContents()
        self.loadTable()

    def loadTable(self):
        data = self.cur.execute('SELECT * FROM coffee')
        data = list(map(lambda x: map(lambda y: str(y), x), data))
        title = "ID,название сорта,степень обжарки,молотый/в зернах,"
        title = (title + "описание вкуса,цена,объем упаковки").split(',')
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()

class AddCoffee(QWidget):
    def __init__(self, ms):
        super().__init__()
        self.ms = ms
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.db = sqlite3.connect('coffee.sqlite')
        self.cur = self.db.cursor()
        self.save.clicked.connect(self.click)

    def click(self):
        name, roasting, _type, description, price, size = (
            self.name.text(), self.roasting.value(),
            self.type.currentText(), self.description.toPlainText(),
            self.price.value(), self.size.value())
        query = "SELECT id FROM coffee WHERE name = ?"
        if self.cur.execute(query, (name,)).fetchall():
            query = """UPDATE coffee SET roasting = ?, type = ?,
            description = ?, price = ?, size = ? WHERE name = ?"""
            self.cur.execute(query, (roasting, _type, description,
                                     price, size, name))
        else:
            query = """INSERT INTO coffee(name, roasting, type,
            description, price, size) VALUES (?, ?, ?, ?, ?, ?)"""
            self.cur.execute(query, (name, roasting, _type,
                                     description, price, size))
        self.db.commit()
        self.ms.update()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())