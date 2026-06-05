from PyQt6.QtWidgets import QWidget

from src.measurments import SugarMeasurementsStore
from ui.graph_ui import Ui_graph


class Graph(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_graph()
        self.ui.setupUi(self)