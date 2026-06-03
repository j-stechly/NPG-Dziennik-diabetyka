from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QDate, QTime

from src.measurments import SugarMeasurementsStore
from ui.add_entry_ui import Ui_add_entry


class AddEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_add_entry()
        self.ui.setupUi(self)

        self.ui.dateInput.setDate(QDate.currentDate())
        self.ui.timeInput.setTime(QTime.currentTime())
        self.ui.sugarLevelInput.setMaximum(1000.00)

        self.ui.addButton.clicked.connect(self.zbierz_dane)

    def zbierz_dane(self):
        poziom_cukru = self.ui.sugarLevelInput.value()
        data = self.ui.dateInput.date().toString("dd.MM.yyyy")
        godzina = self.ui.timeInput.time().toString("HH:mm")

        self.nowy_wpis = {
            "cukier": poziom_cukru,
            "data": data,
            "godzina": godzina
        }

        self.accept()