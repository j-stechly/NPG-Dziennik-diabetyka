from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal  # Dodany import dla własnego sygnału

from src.measurments import SugarMeasurementsStore
from ui.search_ui import Ui_search


class Search(QWidget):
    # Inicjalizacja własnego sygnału (przekazuje wpisany tekst i stan checkboxa)
    search_changed = pyqtSignal(str, bool)

    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_search()
        self.ui.setupUi(self)

        # Zapisujemy store jako zmienną instancji, tak na wszelki wypadek
        self.store = store

        # Łączymy akcje z interfejsu (wpisywanie tekstu, klikanie checkboxa) z naszą funkcją
        self.ui.search_input.textChanged.connect(self.emit_search_params)
        self.ui.sugar_search_checkbox.stateChanged.connect(self.emit_search_params)

    def emit_search_params(self):
        # Pobieramy to, co użytkownik wpisał i zaznaczył
        search_text = self.ui.search_input.text().strip()
        is_sugar_search = self.ui.sugar_search_checkbox.isChecked()

        # Emitujemy (wysyłamy) sygnał dalej, żeby lista pomiarów mogła go odebrać
        self.search_changed.emit(search_text, is_sugar_search)