from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
from collections.abc import Callable
import subprocess
import csv
import json

Converter = Callable[[Path, Path], Path]
REGISTRY: dict[tuple[str, str], Converter] = {}


def converter(source: str, target: str):
    """Dekorator rejestrujący pojedynczy kierunek konwersji."""
    def register(func: Converter) -> Converter:
        REGISTRY[(source.lower(), target.lower())] = func
        return func
    return register


@dataclass(frozen=True)
class ConversionRequest:
    source: Path
    target_format: str
    output_dir: Path

    def validate(self) -> None:
        if not self.source.is_file():
            raise FileNotFoundError("Nie znaleziono pliku wejściowego")
        if not self.output_dir.is_dir():
            raise NotADirectoryError("Nie znaleziono katalogu docelowego")
        key = (self.source.suffix.lower(), self.target_format.lower())
        if key not in REGISTRY:
            raise ValueError(f"Nieobsługiwana konwersja: {key}")


def available_targets(source: Path) -> list[str]:
    return sorted(target for (src, target) in REGISTRY if src == source.suffix.lower())


@converter(".docx", ".pdf")
def docx_to_pdf(source: Path, output_dir: Path) -> Path:
    command = [
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", str(output_dir), str(source)
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Konwersja nie powiodła się")
    target = output_dir / f"{source.stem}.pdf"
    if not target.exists():
        raise RuntimeError("Narzędzie nie utworzyło oczekiwanego pliku")
    return target


def execute(request: ConversionRequest) -> Path:
    request.validate()
    key = (request.source.suffix.lower(), request.target_format.lower())
    # TODO: polityka nadpisywania i rejestrowanie czasu operacji
    return REGISTRY[key](request.source, request.output_dir)


@converter(".csv", ".json")
def csv_to_json(source: Path, output_dir: Path) -> Path:
    target: Path = output_dir / f"{source.stem}.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(source, mode='r', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)

    with open(target, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return target


@converter(".json", ".csv")
def json_to_csv(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(source, mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        raise ValueError(f"Błąd: plik {source.name} nie jest poprawnym plikiem JSON. Plik jest uszkodzony lub błędnie sformatowany.")

    if len(data) == 0:
        raise ValueError("Plik JSON jest pusty, brak danych do konwersji.")

    first_row: list[str] = list(data[0].keys())

    with open(target, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=first_row)
        writer.writeheader()
        writer.writerows(data)

    return target


if __name__ == "__main__":
    test_source_csv = Path("test_csv.csv")
    test_source_json = Path("test_json.json")
    test_error_json = Path("error-json.json")
    test_output_dir = Path("")

    if test_source_csv.exists():
        req_csv_to_json = ConversionRequest(
            source=test_source_csv,
            target_format=".json",
            output_dir=test_output_dir
        )
        json_result = execute(req_csv_to_json)
        print(f"CSV do JSON: zapisano w {json_result}")
    else:
        print(f"Utwórz plik {test_source_csv}. Plik nie był znaleziony.")

    if test_error_json.exists():
        req_json_to_csv = ConversionRequest(
            source=test_error_json,
            target_format=".csv",
            output_dir=test_output_dir
        )
        try:
            csv_result = execute(req_json_to_csv)
        except ValueError as ex:
            print(ex)

    if test_source_json.exists():
        req_json_to_csv = ConversionRequest(
            source= test_source_json,
            target_format=".csv",
            output_dir=test_output_dir
        )
        csv_result = execute(req_json_to_csv)
        print(f"JSON to CSV: zapisano w {csv_result}")
    else:
        print(f"Utwórz plik {test_source_json}. Plik nie był znaleziony.")