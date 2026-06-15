from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from src.measurments import SugarMeasurementsStore
from ui.search_ui import Ui_search


class Search(QWidget):
    """
    A widget responsible for the search bar and filtering options.
    """
    search_changed = pyqtSignal(str, bool)

    def __init__(self, store: SugarMeasurementsStore):
        """
        Initializes the Search widget and connects UI elements to signals.

        Args:
                    store (SugarMeasurementsStore): The main store containing all measurements data.
        """
        super().__init__()
        self.ui = Ui_search()
        self.ui.setupUi(self)

        self.store = store

        self.ui.search_input.textChanged.connect(self.emit_search_params)
        self.ui.sugar_search_checkbox.stateChanged.connect(self.emit_search_params)

    def emit_search_params(self):
        """
        Retrieves current values from the search input and checkbox,
        then emits the 'search_changed' signal with these parameters.

        This method is triggered automatically whenever the user types
        in the search bar or toggles the checkbox.
        """
        search_text = self.ui.search_input.text().strip()
        is_sugar_search = self.ui.sugar_search_checkbox.isChecked()

        self.search_changed.emit(search_text, is_sugar_search)