from PyQt6.QtWidgets import QWidget

from src.measurments import SugarMeasurementsStore
from ui.header_ui import Ui_haeder

class Header(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_haeder()
        self.ui.setupUi(self)

        # Do zapisuwania danych do plików csv użyj funkcji z pliku measurements.py