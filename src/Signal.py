from PyQt5.QtCore import QObject
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

class Signal(QObject):
    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        QApplication.processEvents()

    def flush(self):
        pass