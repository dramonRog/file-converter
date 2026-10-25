from pathlib import Path
from core import ConversionRequest, execute
import converters


def run_test(source: Path, target_format: str, output_dir: Path):
    if not source.exists():
        print(f"Utwórz plik {source}. Plik nie został znaleziony.")
        return

    req = ConversionRequest(
        source=source,
        target_format=target_format,
        output_dir=output_dir
    )

    execute(req)


if __name__ == "__main__":
    test_source_csv = Path("test/csv/test_csv.csv")
    test_source_json = Path("test/json/test_json.json")
    test_error_json = Path("test/json/error-json.json")
    test_source_txt = Path("test/txt/test_text.txt")
    test_source_docx = Path("test/docx/mini-test-doc.docx")
    test_source_odt = Path("test/odt/test_odt.odt")

    output_dir_json = Path("test/json")
    output_dir_csv = Path("test/csv")
    output_dir_pdf = Path("test/pdf")
    output_dir_docx = Path("test/docx")
    output_dir_txt = Path("test/txt")
    output_dir_odt = Path("test/odt")

    print("--- ROZPOCZĘCIE TESTÓW ---")

    run_test(test_source_csv, ".json", output_dir_json)

    run_test(test_error_json, ".csv", output_dir_csv)
    run_test(test_source_json, ".csv", output_dir_csv)

    run_test(test_source_docx, ".pdf", output_dir_pdf)
    run_test(test_source_docx, ".txt", output_dir_txt)
    run_test(test_source_docx, ".odt", output_dir_odt)

    run_test(test_source_txt, ".docx", output_dir_docx)

    run_test(test_source_odt, ".docx", output_dir_docx)

    print("--- KONIEC TESTÓW ---")