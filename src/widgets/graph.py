from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QFont

import pyqtgraph as pg

from src import measurments
from src.measurments import SugarMeasurementsStore
from ui.graph_ui import Ui_graph


class Graph(QWidget):
    """
        Manages graph section of application

        :param store: App data store
    """
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_graph()
        self.ui.setupUi(self)

        self.store = store

        # Define colors
        text_color = self.palette().color(QPalette.ColorRole.Text)
        highlight_color = self.palette().color(QPalette.ColorRole.Highlight)
        base_color = self.palette().color(QPalette.ColorRole.Base)

        # Setup graph
        self.ui.graph_widget.setBackground(base_color)

        # Setup plot item
        p = self.ui.graph_widget.getPlotItem()
        p.setTitle("Poziom cukru [mg/dL]", color=text_color, size="16pt")
        p.setAxisItems({"bottom": pg.DateAxisItem()})
        text_pen = pg.mkPen(color=text_color)
        p.getAxis("left").setTextPen(text_pen)
        p.getAxis("bottom").setTextPen(text_pen)
        p.getAxis("bottom").setFont(QFont("Arial"))
        p.setLabel("left", "Poziom cukru [mg/dL]")
        p.setLabel("bottom", "Data")
        p.showGrid(True, True)

        # Setup plot pens
        self.plot_pen = pg.mkPen(color=highlight_color, width=4)
        self.plot_brush = pg.mkBrush(color=highlight_color)

        # Update ranges and plot
        self.update_date_ranges(reset_values=True)
        self.update_range_button_state()
        self.update_plot()

        # Connect QSignal's
        self.store.measurements_changed.connect(lambda: self.measurements_changed())
        self.ui.from_dateEdit.dateChanged.connect(lambda date: self.from_date_edit_date_changed(date))
        self.ui.to_dateEdit.dateChanged.connect(lambda date: self.to_date_edit_date_changed(date))
        self.ui.date_reset_button.clicked.connect(lambda: self.reset_date_ranges())

    def update_date_ranges(self, reset_values:bool = False) -> None:
        """
            Updates dateEdits allowed date ranges.
            Optionally reset value, so the cover the whole range

            :param reset_values: If True reset the values
        """
        dates = [m.when for m in self.store.measurements]
        if len(dates) == 0:
            return

        date_min = min(dates)
        date_max = max(dates)

        self.ui.from_dateEdit.setDateRange(date_min, date_max)
        self.ui.to_dateEdit.setDateRange(date_min, date_max)

        if reset_values:
            self.reset_date_ranges()

    def reset_date_ranges(self) -> None:
        """Resets dateEdits date ranges, so they cover whole the whole range"""
        date_min = self.ui.from_dateEdit.minimumDate()
        date_max = self.ui.to_dateEdit.maximumDate()

        self.ui.from_dateEdit.setDate(date_min)
        self.ui.to_dateEdit.setDate(date_max)

    def update_range_button_state(self) -> None:
        """
            Enables button if range reset button if full range is not covered.
            Disabled if it is.
        """
        date_min = self.ui.from_dateEdit.minimumDate()
        date_max = self.ui.to_dateEdit.maximumDate()

        disabled = date_min == self.ui.from_dateEdit.date() and date_max == self.ui.to_dateEdit.date()
        self.ui.date_reset_button.setDisabled(disabled)

    def update_plot(self) -> None:
        """Updates plot"""
        from_date = self.ui.from_dateEdit.date().toPyDate()
        to_date = self.ui.to_dateEdit.date().toPyDate()

        measurements = self.store.measurements
        measurements.sort(key=lambda x: x.when)
        x_data = []
        y_data = []
        for m in measurements:
            if from_date <= m.when.date() <= to_date:
                x_data.append(m.when.timestamp())
                y_data.append(m.sugar_level)

        # Scale for symbol
        symbol_size = 4000 / (len(x_data) * len(x_data) + 600) + 5

        p = self.ui.graph_widget.getPlotItem()
        p.clear()
        p.plot(x_data, y_data, pen=self.plot_pen, symbol="o", symbolBrush=self.plot_brush, symbolSize=symbol_size)

    def measurements_changed(self) -> None:
        self.update_date_ranges()
        self.update_range_button_state()
        self.update_plot()

    def from_date_edit_date_changed(self, date: QDate) -> None:
        self.ui.to_dateEdit.setMinimumDate(date)
        self.update_range_button_state()
        self.update_plot()

    def to_date_edit_date_changed(self, date: QDate) -> None:
        self.ui.from_dateEdit.setMaximumDate(date)
        self.update_range_button_state()
        self.update_plot()