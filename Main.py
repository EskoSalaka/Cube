import sys
from PyQt5 import QtWidgets

from MainWindow import Ui_MainWindow

print(1)
def main():
    print(1)
    app = QtWidgets.QApplication(sys.argv)
    print(1)
    ui = Ui_MainWindow()
    print(1)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
