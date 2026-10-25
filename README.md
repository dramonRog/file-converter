# Projekt 1: Uniwersalny konwerter plików

Repozytorium: https://github.com/dramonRog/file-converter

Program zamienia plik z jednego formatu na inny i zapisuje wynik we wskazanym katalogu. Na tym etapie działa z konsoli. Okno w Tkinter pojawi się na kolejnym etapie, więc pliku nie wybiera się jeszcze myszką: skrypt bierze przygotowane ścieżki i woła konwerter z rejestru.

Nie jest to narzędzie do dowolnej zamiany rozszerzeń. Działa tylko dla par z macierzy poniżej. 

Autor: Roman Buchynskyi.

## Co robi program

Są trzy grupy formatów. Logika konwersji jest oddzielona od uruchomienia, więc nową parę dopisuje się do rejestru bez przerabiania całego skryptu.

| Para | Grupa | Narzędzie | Jak przenoszona jest treść |
|---|---|---|---|
| CSV → JSON | dane strukturalne | `csv`, `json` | Pierwszy wiersz jest nagłówkiem. Wynikiem jest lista obiektów w UTF-8, z polskimi znakami. Puste komórki zostają pustymi stringami. Istniejący plik JSON jest nadpisywany. |
| JSON → CSV | dane strukturalne | `csv`, `json` | Wejście musi być listą obiektów. Nagłówek i kolejność kolumn biorą się z kluczy pierwszego obiektu. Pusta lista jest odrzucana. Urwany JSON daje komunikat, a nie przerwanie programu. Istniejący CSV jest nadpisywany. |
| TXT → DOCX | tekst / dokument | python-docx | UTF-8. Każda linia staje się osobnym akapitem. Pusta linia daje pusty akapit. Końcowy znak nowej linii nie dokłada kolejnego pustego akapitu. Znaczniki nie są interpretowane. Istniejący DOCX blokuje zapis. |
| DOCX → TXT | tekst / dokument | python-docx | Do TXT trafiają akapity dokumentu, rozdzielone znakiem nowej linii. Tabele, pola tekstowe, nagłówki i stopki nie są przenoszone. Uszkodzony DOCX jest odrzucany. |
| DOCX → PDF | format biurowy | LibreOffice, tryb headless | Powstaje otwieralny PDF. Układ stron może się różnić od oryginału. Plik, który nie jest prawdziwym DOCX, jest odrzucany przed uruchomieniem LibreOffice. Istniejący PDF blokuje zapis. |
| DOCX → ODT | format biurowy | LibreOffice, tryb headless | Treść tekstowa jest przenoszona, złożony układ może się zmienić. Uszkodzony DOCX jest odrzucany przed uruchomieniem programu. Istniejący ODT blokuje zapis. |
| ODT → DOCX | format biurowy | LibreOffice, tryb headless | Jak wyżej, w drugą stronę. Uszkodzony ODT jest odrzucany. Istniejący DOCX blokuje zapis. |

Przyjęta struktura JSON to lista obiektów o zwykłych wartościach, zapisana w UTF-8. Klucze odpowiadają nagłówkom CSV. Pojedynczy obiekt JSON, zamiast listy, nie jest obsługiwaną strukturą.

LibreOffice jest wołany listą argumentów, bez powłoki, z limitem 60 sekund. Sprawdzany jest kod zakończenia i to, czy plik wynikowy w ogóle powstał i nie jest pusty. Wynik najpierw powstaje w katalogu tymczasowym, a potem jest kopiowany do katalogu docelowego bez nadpisania istniejącego pliku.

## Czego jeszcze nie ma

Nie ma interfejsu graficznego, więc nie ma wyboru pliku ani formatu w oknie. Nie zachowujemy identycznego układu stron, makr, przypisów ani osadzonych wykresów.

Pary dokumentów nie nadpisują istniejącego wyniku i sygnalizują, że plik już jest. CSV i JSON przy kolejnym uruchomieniu zapisują wynik od nowa. JSON inny niż lista obiektów kończy się komunikatem «0». Przy błędzie konwersji `execute()` wypisuje komunikat i zwraca `None`. Brak katalogu docelowego kończy się wyjątkiem jeszcze przed samą konwersją. Konwersje biurowe uruchamia się po kolei. Gdy LibreOffice sprawia kłopot, warto najpierw zamknąć jego otwarte okno.

## Struktura

* `core.py` trzyma rejestr, sprawdzenie ścieżek i wywołanie konwersji.
* `converters.py` zawiera same konwertery.
* `main.py` uruchamia przygotowane kierunki.
* `pyproject.toml` opisuje wersję Pythona i pakiet `python-docx`.
* `test/` zawiera dane wejściowe i przykładowe wyniki.

## Jak uruchomić

Potrzebny jest Python 3.14 lub nowszy oraz zainstalowany LibreOffice. Sam menedżer pakietów Pythona LibreOffice nie doinstaluje. Biblioteka dokumentów nazywa się w instalacji `python-docx`, a w kodzie importuje się ją jako `docx`.

Program szuka LibreOffice po kolei: najpierw w PATH jako `libreoffice`, potem jako `soffice`, a na Windows jeszcze pod `C:\Program Files\LibreOffice\program\soffice.exe`. Do pracy w konsoli na Windows pasuje też `soffice.com` z katalogu `program`. Na macOS typowa ścieżka to `/Applications/LibreOffice.app/Contents/MacOS/soffice`. Gdy programu nie ma, pojawia się prośba o instalację albo ustawienie ścieżki. Nieistniejącą ścieżkę można podać w argumencie `executable` funkcji `docx_to_pdf`. Sam `main.py` tego argumentu nie przyjmuje.

```bash
git clone https://github.com/dramonRog/file-converter.git
cd file-converter
uv sync
uv run python main.py
```

Bez uv:

```bash
python -m venv .venv
```

Po aktywacji środowiska:

```bash
python -m pip install "python-docx>=1.2.0"
python -c "from docx import Document; print('OK')"
python main.py
```

Katalogu `.venv` nie dołącza się do oddawanego archiwum.

`python main.py` przechodzi pary po kolei i zapisuje wynik obok danych w `test/`.

| Wejście | Format | Wynik |
|---|---|---|
| `test/csv/test_csv.csv` | `.json` | `test/json/test_csv.json` |
| `test/json/error-json.json` | `.csv` | komunikat o błędnym JSON, bez pliku |
| `test/json/test_json.json` | `.csv` | `test/csv/test_json.csv` |
| `test/docx/mini-test-doc.docx` | `.pdf` | `test/pdf/mini-test-doc.pdf` |
| `test/docx/mini-test-doc.docx` | `.txt` | `test/txt/mini-test-doc.txt` |
| `test/docx/mini-test-doc.docx` | `.odt` | `test/odt/mini-test-doc.odt` |
| `test/txt/test_text.txt` | `.docx` | `test/docx/test_text.docx` |
| `test/odt/test_odt.odt` | `.docx` | `test/docx/test_odt.docx` |

Dla dokumentów istniejący plik wynikowy blokuje kolejny zapis. Przed ponownym uruchomieniem usuń tylko wyniki, nie pliki wejściowe: `test/pdf/mini-test-doc.pdf`, `test/docx/test_text.docx`, `test/docx/test_text1.docx`, `test/docx/test_odt.docx` i `test/odt/test_text1.odt`. Pary CSV ↔ JSON nadpisują swój wynik same.
