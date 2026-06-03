from PyQt6.QtWidgets import QWidget

from src.measurments import SugarMeasurementsStore
from ui.search_ui import Ui_search

class Search(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_search()
        self.ui.setupUi(self)