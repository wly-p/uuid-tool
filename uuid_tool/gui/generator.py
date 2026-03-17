import tkinter as tk
from tkinter import ttk, messagebox

from ..core import UUIDType, generate


class GeneratorTab(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=16)
        self._build()

    def _build(self) -> None:
        opt_row = ttk.Frame(self)
        opt_row.pack(fill="x", pady=(0, 10))

        ttk.Label(opt_row, text="Type:").pack(side="left")
        self._type_var = tk.StringVar(value=UUIDType.default().label)
        ttk.Combobox(
            opt_row,
            textvariable=self._type_var,
            values=UUIDType.labels(),
            state="readonly",
            width=28,
        ).pack(side="left", padx=(4, 16))

        ttk.Label(opt_row, text="Count:").pack(side="left")
        self._count_var = tk.IntVar(value=10)
        ttk.Spinbox(opt_row, from_=1, to=1000, textvariable=self._count_var, width=6).pack(side="left", padx=(4, 16))

        ttk.Button(opt_row, text="Generate", command=self._generate).pack(side="left")

        self._text = tk.Text(self, width=50, height=16, font=("Courier", 11))
        self._text.pack(fill="both", expand=True)

        copy_row = ttk.Frame(self)
        copy_row.pack(fill="x", pady=(8, 0))
        ttk.Button(copy_row, text="Copy Selection", command=self._copy_sel).pack(side="right", padx=(0, 6))
        ttk.Button(copy_row, text="Copy All", command=self._copy_all).pack(side="right")

        self._generate()

    def _generate(self) -> None:
        uuid_type = UUIDType.from_label(self._type_var.get())
        results = generate(uuid_type, self._count_var.get())
        self._text.delete("1.0", tk.END)
        self._text.insert("1.0", "\n".join(results))

    def _copy_all(self) -> None:
        text = self._text.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", f"Copied {self._count_var.get()} UUIDs to clipboard.")

    def _copy_sel(self) -> None:
        try:
            text = self._text.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(text)
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please select text in the box first.")
