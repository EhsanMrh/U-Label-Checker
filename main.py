import sys
from PyQt5.QtWidgets import *

from gui import MainWindow


if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow(sys.exit)
    Root.show()
    App.exec()

