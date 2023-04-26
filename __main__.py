import sys
import base64
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from src.VSET import MyMainWindow
from assets.logo_bytes import logo_bytes


def get_icon():
    logo_img = base64.b64decode(logo_bytes)
    logo_pixmap = QPixmap()
    logo_pixmap.loadFromData(logo_img)
    return QIcon(logo_pixmap)


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
app.setWindowIcon(get_icon())
myWin = MyMainWindow()
myWin.show()
sys.exit(app.exec_())
