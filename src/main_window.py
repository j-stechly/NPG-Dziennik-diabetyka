from datetime import datetime

from PyQt6.QtWidgets import QMainWindow

from src.widgets.graph import Graph
from src.widgets.footer import Footer
from src.widgets.search import Search
from ui.main_window_ui import Ui_main_window
from src.measurments import SugarMeasurementsStore


class MainWindow(QMainWindow):
    """Main window of application"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.store = SugarMeasurementsStore()

        self.search_widget = Search(self.store)
        self.measurements_list = MeasurementsList(self.store)

        self.ui.search_layout.addWidget(self.search_widget)
        self.ui.search_layout.addWidget(self.measurements_list)

        self.ui.graph_layout.addWidget(Graph(self.store))
        self.ui.footer_layout.addWidget(Footer(self.store))

        
        # Przykład połączenia do sygnału zmiany listy
        # self.store.measurements_changed.connect(lambda: print(f"Measurements changed!: New Size = {len(self.store.measurements)}"))
        # W konsoli widać powiadomienie o zmianie rozmiaru
        # self.store.add_measurement(SugarMeasurement(400.0, datetime.now()))