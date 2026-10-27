from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
import time

Converter = Callable[[Path, Path], Path]
REGISTRY: dict[tuple[str, str], Converter] = {}


def converter(source: str, target: str):
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


def execute(request: ConversionRequest) -> Path | None:
    start_time = time.perf_counter()
    try:
        request.validate()
        key = (request.source.suffix.lower(), request.target_format.lower())

        result_path = REGISTRY[key](request.source, request.output_dir)
        elapsed_time = time.perf_counter() - start_time
        print(f"Sukces. Konwersja {request.source.name} -> {request.target_format} trwała {elapsed_time:.2f} s")
        return result_path
    except Exception as e:
        print(f"Błąd podczas konwersji {request.source.name}: {str(e)}")
        return None
