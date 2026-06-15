from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from ui.measurements_list_ui import Ui_measurements_list
from src.measurments import SugarMeasurement, SugarMeasurementsStore


class MeasurementsList(QWidget):
    """Widget responsible for displaying and deleting sugar measurements."""

    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()

        self.ui = Ui_measurements_list()
        self.ui.setupUi(self)

        self.store = store
        self.table = self.ui.table

        self.configure_table()

        self.store.measurements_changed.connect(self.refresh_table)
        self.refresh_table()

    def configure_table(self) -> None:
        """Configure table appearance and behavior."""
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 56)

    def refresh_table(self) -> None:
        """Refresh table content using current measurements from store."""
        measurements = sorted(
            self.store.measurements,
            key=lambda measurement: measurement.when,
            reverse=True,
        )

        self.table.setRowCount(len(measurements))

        for row, measurement in enumerate(measurements):
            date_item = QTableWidgetItem(measurement.when.strftime("%d.%m.%Y"))
            time_item = QTableWidgetItem(measurement.when.strftime("%H:%M"))
            sugar_level_item = QTableWidgetItem(str(measurement.sugar_level))

            for item in (date_item, time_item, sugar_level_item):
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, time_item)
            self.table.setItem(row, 2, sugar_level_item)

            delete_button = QPushButton("X")
            delete_button.setFixedSize(30, 24)
            delete_button.setToolTip("Usuń wpis")
            delete_button.clicked.connect(
                lambda checked=False, item=measurement: self.delete_measurement(item)
            )

            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(row, 3, button_container)

    def delete_measurement(self, measurement: SugarMeasurement) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle("Usuń wpis")
        msg.setText("Czy na pewno chcesz usunąć ten pomiar?")
        msg.setIcon(QMessageBox.Icon.Question)

        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        msg.button(QMessageBox.StandardButton.Yes).setText("Tak")
        msg.button(QMessageBox.StandardButton.No).setText("Nie")

        msg.exec()

        if msg.clickedButton() == msg.button(QMessageBox.StandardButton.Yes):
            self.store.remove_measurement(measurement)

    def apply_filter(self, search_text: str, is_sugar_search: bool) -> None:
        row_count = self.table.rowCount()
        tolerance = 5.0

        if not search_text:
            for row in range(row_count):
                self.table.setRowHidden(row, False)
            return

        for row in range(row_count):
            if is_sugar_search:
                item = self.table.item(row, 2)
                if item:
                    try:
                        target_value = float(search_text.replace(",", "."))
                        cell_value = float(item.text().replace(",", "."))
                        self.table.setRowHidden(row, abs(target_value - cell_value) > tolerance)
                    except ValueError:
                        self.table.setRowHidden(row, True)
            else:
                item = self.table.item(row, 0)
                if item:
                    self.table.setRowHidden(
                        row,
                        search_text.lower() not in item.text().lower(),
                    )
