import sys
import locale
from PyQt6.QtWidgets import QApplication

from src.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

