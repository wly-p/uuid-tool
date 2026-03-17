import tkinter as tk
from tkinter import ttk

from ..core import validate


class ValidatorTab(ttk.Frame):
    _COLOR_OK = "#1a7f37"
    _COLOR_ERR = "#d1242f"

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=16)
        self._build()

    def _build(self) -> None:
        ttk.Label(self, text="Enter UUIDs (one per line):").pack(anchor="w")

        self._input = tk.Text(self, width=50, height=10, font=("Courier", 11))
        self._input.pack(fill="both", expand=True, pady=(4, 10))

        ttk.Button(self, text="Validate", command=self._validate).pack(anchor="e")

        result_frame = ttk.LabelFrame(self, text="Results", padding=8)
        result_frame.pack(fill="both", expand=True, pady=(10, 0))

        self._result = tk.Text(result_frame, width=50, height=8, font=("Courier", 11), state="disabled")
        self._result.pack(fill="both", expand=True)
        self._result.tag_configure("ok", foreground=self._COLOR_OK)
        self._result.tag_configure("err", foreground=self._COLOR_ERR)

    def _validate(self) -> None:
        raw_lines = self._input.get("1.0", tk.END).strip().splitlines()

        self._result.configure(state="normal")
        self._result.delete("1.0", tk.END)

        if not raw_lines or raw_lines == [""]:
            self._result.insert(tk.END, "(no input)\n", "err")
            self._result.configure(state="disabled")
            return

        results = validate(raw_lines)
        ok = err = 0

        for r in results:
            tag = "ok" if r.valid else "err"
            self._result.insert(tk.END, str(r) + "\n", tag)
            if r.valid:
                ok += 1
            else:
                err += 1

        summary_tag = "ok" if err == 0 else "err"
        self._result.insert(tk.END, f"\n{ok + err} total — {ok} valid, {err} invalid", summary_tag)
        self._result.configure(state="disabled")
