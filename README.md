# 🩸 Dziennik Diabetyka

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)

Kompleksowa aplikacja okienkowa (desktopowa) napisana w języku Python. Narzędzie zostało zaprojektowane z myślą o diabetykach, aby maksymalnie uprościć codzienne monitorowanie poziomu cukru we krwi, analizę trendów oraz zarządzanie historią medyczną.

---

## 📑 Spis treści
1. [Główne funkcjonalności](#-główne-funkcjonalności)
2. [Wykorzystane technologie](#-wykorzystane-technologie)
3. [Struktura i architektura](#-struktura-i-architektura)
4. [Instalacja i uruchomienie](#-instalacja-i-uruchomienie)
5. [Instrukcja obsługi](#-instrukcja-obsługi)
6. [Zespół projektowy](#-zespół-projektowy)

---

## 🚀 Główne funkcjonalności

Aplikacja została podzielona na moduły, które odpowiadają za poszczególne zadania:

* **Zarządzanie wpisami (CRUD):**
  * Szybkie dodawanie nowych pomiarów (wartość poziomu cukru w mg/dL, data, godzina).
  * Usuwanie błędnych wpisów z historii.
* **Wizualizacja analityczna:**
  * Automatycznie generowany, interaktywny wykres liniowy.
  * Oś czasu z automatycznym skalowaniem.
  * Wizualna reprezentacja skoków i spadków poziomu cukru.
* **Wyszukiwanie i filtrowanie:**
  * Wyszukiwanie wpisów po konkretnej dacie lub przedziale czasowym.
  * Możliwość filtrowania wyników po wartościach poziomu cukru.
* **Trwałość danych:**
  * Bezpieczny, lokalny zapis danych w formacie `.csv`.
  * Architektura oparta na obiekcie `Store`, zapewniająca spójność danych we wszystkich widokach aplikacji.
  * Moduł importu i eksportu bazy danych do plików zewnętrznych.

---

## 🛠️ Wykorzystane technologie

Projekt został zbudowany w oparciu o nowoczesny stos technologiczny dla aplikacji desktopowych w Pythonie:

* **Język:** Python 3.10+
* **Interfejs graficzny (GUI):** PyQt6 (wraz z Qt Designerem)
* **Wykresy i wizualizacja:** pyqtgraph
* **Zarządzanie danymi:** Wbudowane moduły `csv`, `datetime`, `os`
* **Zarządzanie wersjami:** Git / GitHub

---

---

## 🏗️ Struktura i architektura

Projekt realizuje podział na warstwę widoku (UI) oraz warstwę logiki biznesowej, wykorzystując wzorzec zarządzania stanem (Store). Drzewo plików prezentuje się następująco:

```text
NPG_project/
├── .venv/                   # Środowisko wirtualne Pythona
├── resources/               # Zasoby statyczne aplikacji
│   └── Icon.ico             # Główna ikona programu
├── src/                     # Logika biznesowa i kontrolery
│   ├── widgets/             # Skrypty obsługujące poszczególne elementy GUI
│   │   ├── add_entry.py
│   │   ├── footer.py
│   │   ├── graph.py
│   │   ├── measurements_list.py
│   │   └── search.py
│   ├── main_window.py       # Kontroler głównego okna
│   └── measurments.py       # Modele danych i SugarMeasurementsStore
├── ui/                      # Pliki widoków XML (Qt Designer) oraz kod Pythona
│   ├── add_entry.ui         
│   ├── add_entry_ui.py
│   ├── footer.ui            
│   ├── footer_ui.py
│   ├── graph.ui             
│   ├── graph_ui.py
│   ├── main_window.ui       
│   ├── main_window_ui.py
│   ├── search.ui            
│   └── search_ui.py
├── .gitignore               # Plik konfiguracyjny Git
├── footer_ui.py             # Zduplikowany plik interfejsu stopki (poza folderem ui)
├── main.py                  # Główny punkt wejścia aplikacji
├── README.md                # Dokumentacja projektu
├── requirements.txt         # Lista zależności systemowych
└── saved_measurements.csv   # Lokalna baza danych (generowana po uruchomieniu, ignorowana przez Git)
```
---

## ⚙️ Instalacja i uruchomienie

Instrukcja krok po kroku, jak uruchomić aplikację lokalnie (dla systemów Windows / Linux / macOS).

**1. Sklonuj repozytorium na swój dysk:**
```bash
git clone [https://github.com/j-stechly/NPG-Dziennik-diabetyka.git]
```
**2. Przejdź do głównego katalogu projektu:**
```bash
cd NPG_project
```
**3. Utwórz i aktywuj wirtualne środowisko (zalecane):**
```bash
Na systemie Windows:
python -m venv .venv
.venv\Scripts\activate

Na systemie Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
```
**4. Zainstaluj wymagane pakiety i biblioteki:**
```bash
pip install -r requirements.txt
```
**5. Uruchom aplikację:**
```bash
python main.py
```
---

## 📖 Instrukcja obsługi

**1. Dodawanie nowego pomiaru**
* Kliknij przycisk **Dodaj wpis** znajdujący się w prawym dolnym rogu ekranu.
* W nowym oknie uzupełnij datę, godzinę oraz poziom cukru, a następnie zatwierdź formularz.
* Nowy pomiar natychmiast zapisze się w bazie i pojawi się na liście oraz na wykresie.

**2. Przeglądanie i usuwanie historii**
* W lewej części aplikacji znajduje się **Lista pomiarów** prezentująca szczegóły wszystkich wpisów.
* Aby usunąć błędnie wprowadzony pomiar, kliknij przycisk **X** znajdujący się na samym końcu odpowiedniego wiersza.

**3. Wyszukiwanie wpisów**
* Skorzystaj z paska **Wyszukiwanie wpisów** w lewym górnym rogu, aby szybko przefiltrować tabelę.
* Domyślnie wyszukiwarka reaguje na wpisywaną datę.
* Zaznacz pole **Wyszukuj po poziomie cukru zamiast po dacie**, jeśli chcesz wyodrębnić pomiary o konkretnej wartości zadeklarowanej w polu wyszukiwania.

**4. Analiza wykresu i zakresu czasowego**
* Panel po prawej stronie wyświetla wykres liniowy, który wizualizuje skoki i spadki poziomu cukru we krwi.
* Poniżej wykresu znajdują się filtry **Od** oraz **Do**, które pozwalają zawęzić renderowane dane do określonego przedziału czasowego.
* Przycisk **Cały zakres** umożliwia szybki powrót do widoku obejmującego kompletną historię.

**5. Zarządzanie bazą danych**
* Przycisk **Exportuj** w dolnym menu pozwala na zgranie obecnej bazy pomiarów do zewnętrznego pliku.
* Przycisk **Importuj** umożliwia wczytanie wcześniej zachowanej historii bezpośrednio do aplikacji.

---

## 👥 Zespół projektowy

Projekt zrealizowany przez zespół w składzie:

* **Jakub Stęchły** – Project Manager (Zarządzanie projektem, architektura aplikacji, klasa `Store`, wykresy)
* **Kacper Smoliński** – Programista (Interfejs i logika dodawania wpisów, dokumentacja `README.md`)
* **Filip Stępień** – Programista (Implementacja modułu eksportu i importu danych)
* **Kornel Szudra** – Programista (Interfejs i logika wyszukiwania / filtrowania wpisów)
* **Karol Stawinoga** – Programista (Moduł wyświetlania listy pomiarów, projekt ikony aplikacji)

---

---