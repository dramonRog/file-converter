import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path

import converters
from core import REGISTRY, ConversionRequest, execute, available_targets


class ConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Uniwersalny Konwerter Plików")
        self.root.geometry("520x270")
        self.root.resizable(False, False)

        self.source_formats = sorted({src for (src, _) in REGISTRY})

        self.source_format = tk.StringVar()
        self.target_format = tk.StringVar()
        self.source_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        self._build_ui()

        if self.source_formats:
            self.source_format.set(self.source_formats[0])
            self.on_source_format_change()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Z formatu:").grid(row=0, column=0, sticky="w", pady=6)
        self.combo_source = ttk.Combobox(
            main_frame, textvariable=self.source_format, values=self.source_formats, state="readonly"
        )
        self.combo_source.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(10, 0), pady=6)
        self.combo_source.bind("<<ComboboxSelected>>", self.on_source_format_change)

        ttk.Label(main_frame, text="Na format:").grid(row=1, column=0, sticky="w", pady=6)
        self.combo_target = ttk.Combobox(
            main_frame, textvariable=self.target_format, state="readonly"
        )
        self.combo_target.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(10, 0), pady=6)

        ttk.Label(main_frame, text="Plik wejściowy:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(main_frame, textvariable=self.source_path, state="readonly").grid(
            row=2, column=1, sticky="ew", padx=(10, 5), pady=6
        )
        ttk.Button(main_frame, text="Wybierz...", command=self.select_file).grid(
            row=2, column=2, sticky="ew", pady=6
        )

        ttk.Label(main_frame, text="Katalog zapisu:").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(main_frame, textvariable=self.output_dir, state="readonly").grid(
            row=3, column=1, sticky="ew", padx=(10, 5), pady=6
        )
        ttk.Button(main_frame, text="Wybierz...", command=self.select_dir).grid(
            row=3, column=2, sticky="ew", pady=6
        )

        self.btn_convert = ttk.Button(main_frame, text="Konwertuj", command=self.start_conversion)
        self.btn_convert.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(18, 8), ipady=3)

        self.lbl_status = ttk.Label(
            main_frame,
            text="Wybierz plik i kliknij Konwertuj",
            wraplength=480,
            justify="left",
            font=("TkDefaultFont", 9, "bold")
        )
        self.lbl_status.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 5))

    def on_source_format_change(self, event=None):
        src_ext = self.source_format.get()

        targets = available_targets(Path(f"plik{src_ext}"))
        self.combo_target["values"] = targets
        self.target_format.set(targets[0] if targets else "")

        current_file = self.source_path.get()
        if current_file and Path(current_file).suffix.lower() != src_ext:
            self.source_path.set("")
            self.lbl_status.config(text=f"Zmieniono format na {src_ext}. Wybierz odpowiedni plik.")

    def select_file(self):
        src_ext = self.source_format.get()
        filetypes = [(f"Pliki {src_ext.upper()}", f"*{src_ext}")]

        filepath = filedialog.askopenfilename(
            title=f"Wybierz plik {src_ext.upper()}",
            filetypes=filetypes
        )
        if filepath:
            path_obj = Path(filepath)
            self.source_path.set(str(path_obj))
            if not self.output_dir.get():
                self.output_dir.set(str(path_obj.parent))
            self.lbl_status.config(text=f"Wybrano: {path_obj.name}")

    def select_dir(self):
        dirpath = filedialog.askdirectory(title="Wybierz katalog zapisu")
        if dirpath:
            self.output_dir.set(str(Path(dirpath)))

    def start_conversion(self):
        src = self.source_path.get()
        tgt = self.target_format.get()
        out = self.output_dir.get()

        if not src:
            messagebox.showwarning("Brak pliku", "Najpierw wybierz plik wejściowy.")
            return
        if not out:
            messagebox.showwarning("Brak katalogu", "Wybierz katalog zapisu.")
            return

        self.btn_convert.config(state=tk.DISABLED)
        self.lbl_status.config(text="Trwa konwersja...")

        threading.Thread(
            target=self._worker,
            args=(Path(src), tgt, Path(out)),
            daemon=True
        ).start()

    def _worker(self, src: Path, tgt: str, out: Path):
        req = ConversionRequest(source=src, target_format=tgt, output_dir=out)
        try:
            result = execute(req, raise_errors=True)
            self.root.after(0, self._on_success, result)
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _on_success(self, result_path: Path):
        self.btn_convert.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"Sukces! Zapisano: {result_path.name}")
        messagebox.showinfo("Sukces", f"Plik został zapisany jako:\n{result_path}")

    def _on_error(self, error_msg: str):
        self.btn_convert.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"Błąd: {error_msg}")
        messagebox.showerror("Błąd konwersji", error_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()