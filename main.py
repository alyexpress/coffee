import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.db = sqlite3.connect('coffee.sqlite')
        self.cur = self.db.cursor()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())