from pathlib import Path
from core import ConversionRequest, execute
import converters


if __name__ == "__main__":
    test_source_csv = Path("test/csv/test_csv.csv")
    test_source_json = Path("test/json/test_json.json")
    test_error_json = Path("test/json/error-json.json")
    test_source_txt = Path("test/txt/test_text.txt")
    test_source_docx = Path("test/docx/test_text1.docx")
    test_source_odt = Path("test/odt/test_odt.odt")

    output_dir_json = Path("test/json")
    output_dir_csv = Path("test/csv")
    output_dir_pdf = Path("test/pdf")
    output_dir_docx = Path("test/docx")
    output_dir_txt = Path("test/txt")
    output_dir_odt = Path("test/odt")

    if test_source_csv.exists():
        req_csv_to_json = ConversionRequest(
            source=test_source_csv,
            target_format=".json",
            output_dir=output_dir_json
        )
        json_result = execute(req_csv_to_json)
        print(f"CSV do JSON: zapisano w {json_result}")
    else:
        print(f"Utwórz plik {test_source_csv}. Plik nie był znaleziony.")

    if test_error_json.exists():
        req_json_to_csv = ConversionRequest(
            source=test_error_json,
            target_format=".csv",
            output_dir=output_dir_csv
        )
        try:
            csv_result = execute(req_json_to_csv)
        except ValueError as ex:
            print(ex)

    if test_source_json.exists():
        req_json_to_csv = ConversionRequest(
            source=test_source_json,
            target_format=".csv",
            output_dir=output_dir_csv
        )
        csv_result = execute(req_json_to_csv)
        print(f"JSON to CSV: zapisano w {csv_result}")
    else:
        print(f"Utwórz plik {test_source_json}. Plik nie był znaleziony.")

    test_source_docx = Path("test/docx/mini-test-doc.docx")

    if test_source_docx.exists():
        req_docx_to_pdf = ConversionRequest(
            source=test_source_docx,
            target_format=".pdf",
            output_dir=output_dir_pdf
        )
        try:
            pdf_result = execute(req_docx_to_pdf)
            print(f"DOCX do PDF: zapisano w {pdf_result}")
        except Exception as e:
            print(f"Błąd konwersji DOCX do PDF: {e}")
    else:
        print(f"Utwórz plik {test_source_docx}. Plik nie był znaleziony.")

    if test_source_txt.exists():
        req_txt_to_docx = ConversionRequest(
            source=test_source_txt,
            target_format=".docx",
            output_dir=output_dir_docx
        )
        try:
            docx_result = execute(req_txt_to_docx)
            print(f"TXT do DOCX: zapisano w {docx_result}")
        except Exception as e:
            print(f"Błąd konwersji TXT do DOCX: {e}")
    else:
        print(f"Utwórz plik {test_source_txt}. Plik nie był znaleziony.")

    if test_source_docx.exists():
        req_docx_to_txt = ConversionRequest(
            source=test_source_docx,
            target_format=".txt",
            output_dir=output_dir_txt
        )
        try:
            txt_result = execute(req_docx_to_txt)
            print(f"DOCX do TXT: zapisano w {txt_result}")
        except Exception as e:
            print(f"Błąd konwersji DOCX do TXT: {e}")

    if test_source_docx.exists():
        req_docx_to_odt = ConversionRequest(
            source=test_source_docx,
            target_format=".odt",
            output_dir=output_dir_odt
        )
        try:
            odt_result = execute(req_docx_to_odt)
            print(f"DOCX do ODT: zapisano w {odt_result}")
        except Exception as e:
            print(f"Błąd konwersji DOCX do ODT: {e}")

    if test_source_odt.exists():
        req_odt_to_docx = ConversionRequest(
            source=test_source_odt,
            target_format=".docx",
            output_dir=output_dir_docx
        )
        try:
            docx_result_from_odt = execute(req_odt_to_docx)
            print(f"ODT do DOCX: zapisano w {docx_result_from_odt}")
        except Exception as e:
            print(f"Błąd konwersji ODT do DOCX: {e}")
    else:
        print(f"Utwórz plik {test_source_odt}. Plik nie był znaleziony.")