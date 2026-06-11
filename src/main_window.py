from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from src.widgets.graph import Graph
from src.widgets.footer import Footer
from src.widgets.search import Search
from ui.main_window_ui import Ui_main_window
from src.measurments import SugarMeasurement, SugarMeasurementsStore
from src.widgets.measurements_list import MeasurementsList


class MainWindow(QMainWindow):
    """Main window of application"""

    def __init__(self):
        super().__init__()

        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.store = SugarMeasurementsStore()

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(Search(self.store))
        left_layout.addWidget(MeasurementsList(self.store))

        self.ui.search_layout.addWidget(left_panel)

        self.ui.graph_layout.addWidget(Graph(self.store))

        self.ui.footer_layout.addWidget(Footer(self.store))

        # Przykład połączenia do sygnału zmiany listy
        # self.store.measurements_changed.connect(
        #     lambda: print(
        #         f"Measurements changed!: New Size = {len(self.store.measurements)}"
        #     )
        # )
        # self.store.add_measurement(SugarMeasurement(400.0, datetime.now()))