from datetime import datetime

from PyQt6.QtWidgets import QWidget, QDialog, QFileDialog

from src.widgets.add_entry import AddEntryDialog
from ui.footer_ui import Ui_footer
from src.measurments import (
    SugarMeasurementsStore, 
    SugarMeasurement, 
    read_measurements_from_csv, 
    write_measurements_to_csv
)


class Footer(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_footer()
        self.ui.setupUi(self)
<<<<<<< HEAD
        self.store = store
=======
        self.store=store
>>>>>>> 1836abe96fa350993ad366b70cc15cd7f64c2363

        self.ui.add_entry_button.clicked.connect(self.open_add_entry_dialog)
        self.ui.export_button.clicked.connect(self.export_data)
        self.ui.import_button.clicked.connect(self.import_data)
        # Do zapisuwania danych do plików csv użyj funkcji z pliku measurements.py

    def open_add_entry_dialog(self):
            dialog = AddEntryDialog()

            if dialog.exec() == QDialog.DialogCode.Accepted:
                dane = dialog.nowy_wpis

                datetime_str = f"{dane['data']} {dane['godzina']}"

                measurement_time = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")

                new_measurement = SugarMeasurement(level=dane['cukier'], when=measurement_time)
                self.store.add_measurement(new_measurement)
<<<<<<< HEAD


    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Eksportuj pomiary",
            "",
            "Pliki CSV (*.csv);;Wszystkie pliki (*)"
        )
        
        if file_path:
            current_measurements = self.store.measurements
            write_measurements_to_csv(file_path, current_measurements)

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importuj pomiary",
            "",
            "Pliki CSV (*.csv);;Wszystkie pliki (*)"
        )
        
        if file_path:
            imported_measurements = read_measurements_from_csv(file_path)
            
            if imported_measurements:
                self.store.measurements = imported_measurements
=======
>>>>>>> 1836abe96fa350993ad366b70cc15cd7f64c2363
