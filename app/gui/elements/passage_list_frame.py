import tkinter as tk
from app.gui.elements.passage_list_tree import PassageListTree

class PassageListFrame(tk.Frame):
    def __init__(self, root, parser, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.parser = parser
        self.passages_list_tree = PassageListTree(self, self.parser)
        scrollbar = tk.Scrollbar(self)
        self.passages_list_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.passages_list_tree.yview)


        self.passages_list_tree.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")