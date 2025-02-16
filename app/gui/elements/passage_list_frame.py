import tkinter as tk
from app.gui.elements.passage_listbox import PassageListbox

class PassageListFrame(tk.Frame):
    def __init__(self, root, parser, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.parser = parser
        self.passages_listbox = PassageListbox(self, self.parser)
        self.passages_listbox.generate_passages_listbox()
        scrollbar = tk.Scrollbar(self)
        self.passages_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.passages_listbox.yview)

        passages_list_buttons = tk.Frame(self)
        natural_order_button = tk.Button(passages_list_buttons, text="Normal order",
                                         command=self.passages_listbox.generate_passages_listbox)
        alpha_order_button = tk.Button(passages_list_buttons, text="Alphabetical order",
                                       command=lambda: self.passages_listbox.generate_passages_listbox("alpha"))

        natural_order_button.pack(side="left")
        alpha_order_button.pack(side="left")
        passages_list_buttons.pack(side="bottom", fill="x")
        self.passages_listbox.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")