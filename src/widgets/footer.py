from datetime import datetime

from PyQt6.QtWidgets import QWidget, QDialog

from src.measurments import SugarMeasurementsStore
from src.widgets.add_entry import AddEntryDialog
from ui.footer_ui import Ui_footer
from src.measurments import SugarMeasurement


class Footer(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_footer()
        self.ui.setupUi(self)
        self.store=store

        self.ui.add_entry_button.clicked.connect(self.open_add_entry_dialog)
        # Do zapisuwania danych do plików csv użyj funkcji z pliku measurements.py

    def open_add_entry_dialog(self):
            dialog = AddEntryDialog()

            if dialog.exec() == QDialog.DialogCode.Accepted:
                dane = dialog.nowy_wpis

                datetime_str = f"{dane['data']} {dane['godzina']}"

                measurement_time = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")

                new_measurement = SugarMeasurement(level=dane['cukier'], when=measurement_time)
                self.store.add_measurement(new_measurement)
