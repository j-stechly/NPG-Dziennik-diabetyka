from PyQt6.QtWidgets import QWidget

from src.measurments import SugarMeasurementsStore
from ui.header_ui import Ui_haeder

class Header(QWidget):
    def __init__(self, store: SugarMeasurementsStore):
        super().__init__()
        self.ui = Ui_haeder()
        self.ui.setupUi(self)

        # Poniższy kod może się przydać przy zapisywaniu danych do pliku .csv
        # Uwaga należy użyć obiektu ze store'ga
        # === Zapis do pliku CSV ===
        # nazwa_pliku = 'pomiary.csv'
        # plik_istnieje = os.path.isfile(nazwa_pliku)
        #
        # with open(nazwa_pliku, mode='a', newline='', encoding='utf-8') as plik:
        #     pola = ['data', 'godzina', 'cukier']
        #     writer = csv.DictWriter(plik, fieldnames=pola)
        #
        #     if not plik_istnieje:
        #         writer.writeheader()
        #
        #     writer.writerow(dane)
        #
        # print("Zapisano nowy pomiar do pliku pomiary.csv!")