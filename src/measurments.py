from datetime import datetime
from typing import Collection

from PyQt6.QtCore import pyqtSignal, QObject


class SugarMeasurement:
    def __init__(self, level: float, when: datetime):
        """
            Contains info about sugar level in blood.

            :param self: Object
            :param level: Level of sugar in blood
            :param when: datetime associated with measurement
        """
        self.level_ = level
        self.when = when

class SugarMeasurementsStore(QObject):
    # Signal responsible for announcing change in measurement list
    measurements_changed = pyqtSignal(list)

    def __init__(self, load_data: bool = True):
        """
            Stores sugar level measurements

            :param self: Object
            :param load_data: If True load data from disk
        """
        super().__init__()
        self._measurements = []
        if load_data:
            self.load_data()

    @property
    def measurements(self) -> Collection[SugarMeasurement]:
        """
            Creates shallow copy of stored measurements.

            :param self: Object
            :return: Shallow copy of stored measurements
        """
        return self._measurements.copy()

    @measurements.setter
    def measurements(self, measurements: Collection[SugarMeasurement]) -> None:
        """
            Sets new measurements

            :param self: Object
            :param measurements: List of new measurements
        """
        self._measurements = measurements
        self.measurements_changed.emit(measurements)


    def add_measurement(self, measurement: SugarMeasurement) -> None:
        """
            Adds measurement.

            :param measurement: Measurement to add
        """
        self._measurements.append(measurement)
        self.measurements_changed.emit(self._measurements.copy())

    def remove_measurement(self, measurement: SugarMeasurement) -> None:
        """
            Removes measurement.

            :param measurement: Measurement to remove
        """
        if measurement in self.measurements:
            self._measurements.remove(measurement)
            self.measurements_changed.emit(self._measurements.copy())

    def load_data(self) -> None:
        """Loads data from disk."""
        # Mock data
        self._measurements = [
            SugarMeasurement(100, datetime.now()),
            SugarMeasurement(200, datetime.now()),
            SugarMeasurement(300, datetime.now())
        ]
        self.measurements_changed.emit(self._measurements.copy())

    def save_data(self) -> None:
        """Saves data to disk."""
        pass
