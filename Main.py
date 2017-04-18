import sys

import PyQt5.QtGui

from MainWindow import Ui_MainWindow


def main():
    app = PyQt5.QtGui.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
