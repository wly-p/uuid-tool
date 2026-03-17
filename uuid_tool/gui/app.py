import tkinter as tk
from tkinter import ttk

from .generator import GeneratorTab
from .validator import ValidatorTab


class UUIDApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("UUID Tool")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(GeneratorTab(notebook), text="  Generate  ")
        notebook.add(ValidatorTab(notebook), text="  Validate  ")
