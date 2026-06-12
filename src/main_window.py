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

        # Tworzenie lewego panelu layoutu
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Inicjalizacja widgetów jako zmienne instancji klasy
        self.search_widget = Search(self.store)
        self.measurements_list = MeasurementsList(self.store)

        # Dodanie widgetów do układu pionowego
        left_layout.addWidget(self.search_widget)
        left_layout.addWidget(self.measurements_list)

        # Podpięcie panelu do głównego układu okna
        self.ui.search_layout.addWidget(left_panel)

        self.ui.graph_layout.addWidget(Graph(self.store))

        self.ui.footer_layout.addWidget(Footer(self.store))

        # POŁĄCZENIE SYGNAŁU: Przekazanie filtrów z wyszukiwarki do listy wpisów
        self.search_widget.search_changed.connect(self.measurements_list.apply_filter)

        # Przykład połączenia do sygnału zmiany listy
        # self.store.measurements_changed.connect(
        #     lambda: print(
        #         f"Measurements changed!: New Size = {len(self.store.measurements)}"
        #     )
        # )
        # self.store.add_measurement(SugarMeasurement(400.0, datetime.now()))