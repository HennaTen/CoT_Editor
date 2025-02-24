import tkinter as tk
from tkinter import filedialog, ttk
from app.parser.cot_parser import CoTParser
from app.gui.passage_frame import PassageFrame


class MainGUI:
    def __init__(self, path):
        self.root = tk.Tk()
        self.root.title("CoT Editor")
        self.root.state('zoomed')

        self.parser = CoTParser(path)
        self.passages_data = self.parser.passages_data

        tab_control = ttk.Notebook(self.root)
        self.elements = {
            "passage_frame": PassageFrame(tab_control, self.passages_data)
        }
        tab_control.add(self.elements["passage_frame"].frame, text='Passages')
        tab_control.pack(expand=1, fill="both")
        # self.setup_ui()  # TODO: Not implemented

    def setup_ui(self):  # TODO: Not implemented

        def setup_menu():
            menubar = tk.Menu(self.root)
            file_menu = tk.Menu(menubar, tearoff=0)

            def open_directory():
                directory = filedialog.askdirectory()
                if directory:
                    pass

            file_menu.add_command(label="Open Project", command=open_directory)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            menubar.add_cascade(label="File", menu=file_menu)
            self.root.config(menu=menubar)

        setup_menu()

    def run(self):
        self.root.mainloop()
