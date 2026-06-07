from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QDialog

from src.widgets.graph import Graph
from src.widgets.header import Header
from src.widgets.search import Search
from ui.main_window_ui import Ui_main_window
from src.widgets.add_entry import AddEntryDialog
from src.measurments import SugarMeasurement, SugarMeasurementsStore



class MainWindow(QMainWindow):
    """Main window of application"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.store = SugarMeasurementsStore()

        self.ui.header_layout.addWidget(Header(self.store))
        self.ui.search_layout.addWidget(Search(self.store))
        self.ui.graph_layout.addWidget(Graph(self.store))

        self.ui.add_entry_button.clicked.connect(self.open_add_entry_dialog)
        # Przykład połączenia do sygnału zmiany listy
        # self.store.measurements_changed.connect(lambda: print(f"Measurements changed!: New Size = {len(self.store.measurements)}"))
        # W konsoli widać powiadomienie o zmianie rozmiaru
        # self.store.add_measurement(SugarMeasurement(400.0, datetime.now()))

    def open_add_entry_dialog(self):
        dialog = AddEntryDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            dane = dialog.nowy_wpis

            datetime_str = f"{dane['data']} {dane['godzina']}"

            measurement_time = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")

            new_measurement = SugarMeasurement(level=dane['cukier'], when=measurement_time)
            self.store.add_measurement(new_measurement)