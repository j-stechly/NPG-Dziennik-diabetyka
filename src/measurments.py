import csv
import os
from datetime import datetime
from typing import List

from PyQt6.QtCore import pyqtSignal, QObject


class SugarMeasurement:
    def __init__(self, level: float, when: datetime):
        """
            Contains info about sugar level in blood.

            :param self: Object
            :param level: Level of sugar in blood
            :param when: datetime associated with measurement
        """
        self.sugar_level = level
        self.when = when

SAVED_MEASUREMENTS_PATH = "saved_measurements.csv"

class SugarMeasurementsStore(QObject):
    # Signal responsible for announcing change in measurements list
    measurements_changed = pyqtSignal()

    def __init__(self):
        """
            Stores sugar level measurements.
            Load measurements data from disk at object creation.
        """
        super().__init__()
        self._measurements = read_measurements_from_csv(SAVED_MEASUREMENTS_PATH)

    @property
    def measurements(self) -> List[SugarMeasurement]:
        """
            Creates shallow copy of stored measurements.

            :return: Shallow copy of stored measurements
        """
        return self._measurements.copy()

    @measurements.setter
    def measurements(self, measurements: List[SugarMeasurement]) -> None:
        """
            Sets new measurements

            :param measurements: List of new measurements
        """
        if measurements is not self._measurements:
            self._measurements = measurements
            self.measurements_changed.emit()
            write_measurements_to_csv(SAVED_MEASUREMENTS_PATH, measurements)

    def add_measurement(self, measurement: SugarMeasurement) -> None:
        """
            Adds measurement.

            :param measurement: Measurement to add
        """
        self._measurements.append(measurement)
        self.measurements_changed.emit()
        write_measurements_to_csv(SAVED_MEASUREMENTS_PATH, [measurement], True)

    def remove_measurement(self, measurement: SugarMeasurement) -> None:
        """
            Removes measurement.

            :param measurement: Measurement to remove
        """
        if measurement in self._measurements:
            self._measurements.remove(measurement)
            self.measurements_changed.emit()
            write_measurements_to_csv(SAVED_MEASUREMENTS_PATH, self._measurements)

def read_measurements_from_csv(path: str) -> List[SugarMeasurement]:
    """
        Read measurements from csv file at specified path

        :param path: Path to load data from
        :return: List of measurements
    """
    if not os.path.isfile(path):
        return []

    with open(path, "r") as file:
        data = file.readlines()

        measurements: list[SugarMeasurement] = []
        for row in data[1:]:
            try:
                split = row.rfind(",")
                when = datetime.strptime(row[:split], "%d.%m.%Y,%H:%M")
                sugar_level = float(row[split + 1:])
            except (IndexError, ValueError):
                print(f"Failed to parse row[{row}] from path[{path}]")
                continue

            m = SugarMeasurement(sugar_level, when)
            measurements.append(m)

        return measurements

def write_measurements_to_csv(path: str, measurements: List[SugarMeasurement], append: bool = False) -> None:
    """
        Writes measurements data to disk at specified path.

        :param path: Path to save data to
        :param measurements: Measurements to save
        :param append: If True appends to end of file instead of rewriting
    """
    data = [
        {
            "date": m.when.date().strftime("%d.%m.%Y"),
            "time": m.when.time().strftime("%H:%M"),
            "sugar_level": m.sugar_level
        }
        for m in measurements
    ]

    file_exists = os.path.isfile(path)
    mode = "a" if append else "w"
    with open(path, mode=mode, newline="", encoding="utf-8") as file:
        fields = ["date", "time", "sugar_level"]
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists or not append:
            writer.writeheader()

        writer.writerows(data)
