from dataclasses import dataclass
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