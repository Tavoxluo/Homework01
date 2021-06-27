from PyQt5 import QtWidgets
from UIWriter import emailWriter
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = emailWriter()
    mw = QtWidgets.QWidget()
    win.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
