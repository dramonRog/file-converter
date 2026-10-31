# Uniwersalny konwerter plików

Repozytorium: https://github.com/dramonRog/file-converter

Program z oknem, w którym wybiera się plik, katalog zapisu i format docelowy. Lista formatów zależy od rozszerzenia źródła: widać tylko pary, które konwerter naprawdę obsługuje. Po kliknięciu „Konwertuj” wynik trafia do wybranego katalogu. Jeśli plik o tej nazwie już tam jest, program go nie zastępuje.

Autor: Roman Buchynskyi.

## Technologie

* **Python 3.14** albo nowszy. Interfejs korzysta z biblioteki standardowej **Tkinter** i **ttk**, bez dodatkowych pakietów do okien.
* **python-docx** (import w kodzie: `docx`) do TXT ↔ DOCX.
* **LibreOffice** w trybie bez okna do DOCX → PDF, DOCX → ODT i ODT → DOCX. To program systemowy. Sam `pip` go nie instaluje.
* Moduły standardowe `csv`, `json`, `pathlib`, `subprocess` i `zipfile` do danych tabelarycznych, ścieżek i uruchomienia procesu.

Konwertery są w rejestrze, osobno od okna. Nowa para formatów nie wymaga przebudowy interfejsu: lista „Na format” czyta ten rejestr.

## Co potrafi

Program nie zamienia dowolnych rozszerzeń. JSON musi być listą obiektów w UTF-8. Klucze odpowiadają nagłówkom CSV, a kolejność kolumn bierze się z pierwszego obiektu. W pliku TXT każda linia staje się akapitem DOCX. Pusta linia zostaje pustym akapitem, a sam znak nowej linii na końcu nie dokłada kolejnego.

| Para | Grupa | Narzędzie | Co zostaje z treści |
|---|---|---|---|
| CSV → JSON | dane strukturalne | `csv`, `json` | Pierwszy wiersz jest nagłówkiem. Wynik to lista obiektów. Polskie znaki zostają. Istniejący plik blokuje zapis. |
| JSON → CSV | dane strukturalne | `csv`, `json` | Nagłówek i kolejność kolumn z pierwszego obiektu. Pusta lista i urwany JSON dają komunikat. Istniejący plik blokuje zapis. |
| TXT → DOCX | tekst i dokument | python-docx | Linia po linii, razem z pustymi akapitami. Istniejący DOCX blokuje zapis. |
| DOCX → TXT | tekst i dokument | python-docx | Zwykłe akapity, rozdzielone nową linią. Pola tekstowe, tabele i stopki nie przechodzą. |
| DOCX → PDF | format biurowy | LibreOffice | Otwieralny PDF. Układ stron może się różnić. Plik, który nie jest prawdziwym DOCX, jest odrzucany. |
| DOCX → ODT | format biurowy | LibreOffice | Tekst przechodzi, złożony układ może się zmienić. |
| ODT → DOCX | format biurowy | LibreOffice | Jak wyżej, w drugą stronę. |

LibreOffice jest szukany w PATH jako `libreoffice`, potem jako `soffice`, a na Windows jeszcze w `C:\Program Files\LibreOffice\program\soffice.exe`. Na macOS typowa ścieżka to `/Applications/LibreOffice.app/Contents/MacOS/soffice`. Proces dostaje argumenty osobno, bez powłoki, z limitem 60 sekund. Sam kod zakończenia równy zero nie wystarcza: plik wynikowy musi powstać i nie być pusty.

## Jak korzystać z okna

1. Wybierz rozszerzenie źródła („Z formatu”). Lista „Na format” pokazuje tylko dozwolone cele.
2. Wskaż plik tego typu i katalog zapisu. Jeśli katalog jest pusty, program proponuje folder wybranego pliku.
3. Kliknij „Konwertuj”. Na czas pracy przycisk jest wyłączony, a status pokazuje, że konwersja trwa.
4. Sukces kończy się oknem ze ścieżką zapisu. Błąd, brak pliku, brak katalogu, uszkodzone dane albo istniejący wynik pokazują przyczynę i nie zostawiają cichego nadpisania.

Zmiana formatu źródła czyści wcześniej wybrany plik, jeśli ma inne rozszerzenie.

## Instalacja i uruchomienie

Potrzebny jest Python 3.14+ oraz LibreOffice, jeśli mają działać pary biurowe.

```bash
git clone https://github.com/dramonRog/file-converter.git
cd file-converter
uv sync
uv run python gui.py
```

Bez uv:

```bash
python -m venv .venv
```

Po aktywacji środowiska:

```bash
python -m pip install "python-docx>=1.2.0"
python gui.py
```

Katalogu `.venv` nie dodaje się do archiwum projektu.

`python main.py` zostawia starszą ścieżkę konsolową: przechodzi przygotowane pliki z katalogu `test/` i wypisuje wynik w terminalu. Do zwykłej pracy służy okno.

## Struktura

* `gui.py` to okno Tkinter/ttk.
* `core.py` trzyma rejestr, sprawdzenie ścieżek i wywołanie konwersji.
* `converters.py` zawiera same konwertery.
* `main.py` uruchamia zestaw prób bez okna.
* `pyproject.toml` opisuje wersję Pythona i `python-docx`.
* `test/` zawiera przykładowe pliki wejściowe i wyniki.

## Ograniczenia

Identyczny układ stron, makra, przypisy i osadzone wykresy nie są celem programu. DOCX → TXT nie widzi tekstu schowanego w polach tekstowych. JSON inny niż lista obiektów, na przykład pojedynczy obiekt, nie jest przyjętą strukturą. Konwersje przez LibreOffice lepiej uruchamiać po kolei. Gdy program biurowy sprawia kłopot, warto najpierw zamknąć jego otwarte okno.

## Dalsze kroki

* Testy automatyczne dla sprawdzenia ścieżek, listy formatów i co najmniej dwóch konwerterów.
* Czytelniejszy komunikat, gdy JSON jest poprawny składniowo, ale nie jest listą obiektów.
* Ewentualne pytanie „czy zastąpić istniejący plik?” zamiast samej odmowy zapisu.
