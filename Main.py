import sys
from PyQt5 import QtWidgets
import pprint
from Base import PCard
from Base.PCardList import PCardList
from MainWindow import Ui_MainWindow
from Database import ZODBTools
from persistent.list import PersistentList
import timeit
import transaction
from mtgsdk import Card


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
