from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QAbstractItemView,
    QPushButton,
    QMessageBox,
)

from PyQt6.QtCore import Qt

from src.measurments import SugarMeasurement, SugarMeasurementsStore


class MeasurementsList(QWidget):
     """
        Widget responsible for displaying sugar measurements in table.

        Allows user to:
        - display saved measurements,
        - sort measurements by date,
        - delete selected measurement,
        - filter measurements by date or sugar level.

        :param QWidget: Base Qt widget class
    """     

def __init__(self, store: SugarMeasurementsStore):
        """
            Creates measurements list widget.

            Initializes table, title label and layout.
            Connects store signal with table refresh method.

            :param self: Object
            :param store: Object responsible for storing sugar measurements
        """
        super().__init__()
        self.store = store

        self.title_label = QLabel("Lista pomiarów")

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
        self.table.setStyleSheet(
            """
            QTableWidget::item {
                padding-left: 10px;
                padding-right: 10px;
            }

            QTableWidget::item:selected {
                background-color: #3a3a3a;
            }

            QPushButton {
                min-width: 30px;
                max-width: 30px;
                min-height: 24px;
                max-height: 24px;
                padding: 0px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)

        self.store.measurements_changed.connect(self.refresh_table)
        self.refresh_table()

def refresh_table(self) -> None:
        """
            Refreshes table content using current measurements from store.

            Measurements are sorted by date from newest to oldest.
            For each measurement one row is created.

            :param self: Object
            :return: None
        """
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
        """
            Removes selected measurement after user confirmation.

            If user clicks "Tak", measurement is removed from store.

            :param self: Object
            :param measurement: Measurement selected for deletion
            :return: None
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Usuń wpis")
        msg.setText("Czy na pewno chcesz usunąć ten pomiar?")
        msg.setIcon(QMessageBox.Icon.Question)

        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.store.remove_measurement(measurement)

def apply_filter(self, search_text: str, is_sugar_search: bool):
        """
        Filters the visible rows in the table based on the search criteria.

        If 'is_sugar_search' is True, it filters by sugar level allowing
        a tolerance of +/- 5 from the target value. Otherwise, it performs
        a standard text search on the date column.

        Args:
            search_text (str): The text or number entered by the user.
            is_sugar_search (bool): True if searching by sugar level, False if by date.
        """
        row_count = self.table.rowCount()

        # Fixed tolerance value for sugar level search (+/- 10)
        tolerance = 5.0

        # If the search field is empty, show all rows
        if not search_text:
            for row in range(row_count):
                self.table.setRowHidden(row, False)
            return

        for row in range(row_count):
            if is_sugar_search:
                item = self.table.item(row, 2)  # Column 2: Sugar level
                if item:
                    try:
                        # Convert input and table texts to floats
                        # (.replace() handles comma separators)
                        target_value = float(search_text.replace(',', '.'))
                        cell_value = float(item.text().replace(',', '.'))

                        # Show row if the difference is within the tolerance
                        if abs(target_value - cell_value) <= tolerance:
                            self.table.setRowHidden(row, False)
                        else:
                            self.table.setRowHidden(row, True)

                    except ValueError:
                        # Hide the row if the user inputs invalid data (e.g., letters)
                        self.table.setRowHidden(row, True)
            else:
                # Traditional text search (e.g., for dates)
                item = self.table.item(row, 0)  # Column 0: Date
                if item:
                    if search_text.lower() in item.text().lower():
                        self.table.setRowHidden(row, False)
                    else:
                        self.table.setRowHidden(row, True)