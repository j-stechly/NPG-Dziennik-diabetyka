import sys
import csv
import os
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

from App_ui import Ui_MainWindow
from add_entry import AddEntryDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.otworz_okno_dodawania)

    def otworz_okno_dodawania(self):
        dialog = AddEntryDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            dane = dialog.nowy_wpis

            # === Zapis do pliku CSV ===
            nazwa_pliku = 'pomiary.csv'
            plik_istnieje = os.path.isfile(nazwa_pliku)

            with open(nazwa_pliku, mode='a', newline='', encoding='utf-8') as plik:
                pola = ['data', 'godzina', 'cukier']
                writer = csv.DictWriter(plik, fieldnames=pola)

                if not plik_istnieje:
                    writer.writeheader()

                writer.writerow(dane)

            print("Zapisano nowy pomiar do pliku pomiary.csv!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())