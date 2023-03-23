from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from typing import Optional

#from  Mywidget import MListWidget,MLineEdit

class MListWidget(QtWidgets.QListWidget):
    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)            # 设置拖放
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择多个
        self.setDefaultDropAction(Qt.CopyAction)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """（从外部或内部控件）拖拽进入后触发的事件"""
        # print(e.mimeData().text())
        if e.mimeData().hasText():
            if e.mimeData().text().startswith('file:///'):
                e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """拖拽移动过程中触发的事件"""
        e.accept()

    def dropEvent(self, e: QDropEvent) -> None:
        """拖拽结束以后触发的事件"""
        paths = e.mimeData().text().split('\n')
        for path in paths:
            path = path.strip()
            if len(path) > 8:
                self.addItem(path.strip()[8:])
        e.accept()

class MLineEdit(QtWidgets.QLineEdit):#实现可拖拽导入输出路径
    def __init__(self, title):
        super().__init__(title)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')[0] #拖拽多文件只取第一个地址
        filePath = filePath.replace('file:///', '', 1) #去除文件地址前缀的特定字符
        self.setText(filePath)