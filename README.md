# Projekt 1: Uniwersalny konwerter plików

Aplikacja desktopowa napisana w języku Python, pozwalająca na łatwą i bezpieczną konwersję plików między różnymi formatami.

**Autor:** Roman Buchynskyi  
**Technologia bazowa:** Python 3 + Tkinter/ttk

---

## Cel projektu
Stworzenie narzędzia, które pozwala wybrać plik wejściowy, pokazuje dostępne dla niego formaty docelowe, wykonuje konwersję i zapisuje wynik. Logika konwersji jest całkowicie oddzielona od interfejsu użytkownika (wzorzec Rejestru).

---

## Wymagania i instalacja

Projekt wykorzystuje najnowsze standardy zarządzania zależnościami w Pythonie (`pyproject.toml` oraz `uv`).

### Wymagania systemowe
* **Python:** wersja 3.10 lub nowsza.
* **System operacyjny:** Windows / Linux / macOS.

### Instalacja i uruchomienie
1. Sklonuj repozytorium na swój komputer:

   ```bash
   git clone https://github.com/dramonRog/file-converter.git
   cd file-converter
   ```

2. Projekt korzysta wyłącznie z wbudowanych bibliotek Pythona dla obecnych konwerterów. Nie ma potrzeby instalowania dodatkowych pakietów.
3. Aby uruchomić testową konwersję bez GUI, użyj polecenia:
    ```bash
    python main.py
    ```
---

## Status i obsługiwane formaty

Aplikacja jest rozwijana etapami. Głównym założeniem jest obsługa trzech grup formatów: danych strukturalnych, tekstowych oraz biurowych.

### Funkcje zrealizowane

Zaimplementowano w pełni konwertery danych strukturalnych:

* **CSV do JSON**
* *Opis:* Konwertuje dane tabelaryczne z pierwszego wiersza (nagłówki) na listę obiektów JSON.
* *Ograniczenia:* Wymaga poprawnego formatowania znaków specjalnych w komórkach za pomocą cudzysłowów (zgodnie ze standardem CSV).


* **JSON do CSV**
* *Opis:* Pobiera strukturę na podstawie pierwszego obiektu z listy i generuje plik tabelaryczny.
* *Zabezpieczenia:* Aplikacja nie ulega awarii przy podaniu nieprawidłowego pliku – rzuca kontrolowany wyjątek. Puste pliki JSON są poprawnie identyfikowane i odrzucane z odpowiednim komunikatem.



W obu kierunkach zagwarantowano bezstratne przenoszenie polskich znaków diakrytycznych (kodowanie UTF-8) i prewencję przed nadmiarowymi pustymi wierszami.

### Planowane do realizacji

W kolejnych etapach dodane zostaną:

* Konwersja dokumentów tekstowych (np. TXT → DOCX / PDF).
* Wsparcie formatów biurowych wykorzystujące silnik LibreOffice w trybie headless.

---

## Scenariusze testowe

Dla celów walidacji projektu przygotowano dedykowane pliki w folderze głównym oraz skrypt uruchomieniowy w `main.py`. Aplikację można zweryfikować manualnie bez GUI.

**Opis przygotowanych danych:**

1. **Plik `test_csv.csv`**
* Zawiera wykaz projektów informatycznych.
* *Cel testu:* Sprawdzenie czy znaki takie jak `żółć, gęślą, jaźń` są konwertowane na obiekt JSON bez błędów strukturalnych (np. niepożądanego rozbijania na dodatkowe kolumny/klucze typu null).


2. **Plik `test_json.json`**
* Zawiera zbiór trójwymiarowych modeli programu Blender.
* *Cel testu:* Weryfikacja umiejętności zdekodowania JSON i zbudowania nagłówków dla pliku wyjściowego CSV.


3. **Uszkodzony plik `error-json.json`**
* Zawiera uszkodzoną strukturę symulującą wadliwe dane wejściowe.
* *Cel testu:* Prezentacja prawidłowej obsługi wyjątków - pojawienie się w konsoli komunikatu "Błąd: plik nie jest poprawnym plikiem JSON", zamiast awarii interpretera Pythona.



Aby przetestować wszystkie scenariusze i automatycznie sprawdzić zapis plików wyjściowych, należy użyć komendę: `python main.py`
