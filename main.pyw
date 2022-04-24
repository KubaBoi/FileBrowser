from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:7999/"))

        self.setCentralWidget(self.browser)

        self.show()

app = QApplication(sys.argv)
window = MainWindow()
window.resize(1200, 700)

app.exec_()