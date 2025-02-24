import tkinter as tk
from app.gui.elements.passage_list_tree import PassageListTree

class PassageListFrame(tk.Frame):
    def __init__(self, root, parser, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.parser = parser
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search)
        self.search_bar = tk.Entry(self, textvariable=self.search_var)
        self.passages_list_tree = PassageListTree(self, self.parser)
        scrollbar = tk.Scrollbar(self)
        self.passages_list_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.passages_list_tree.yview)

        self.search_bar.pack(side="top", fill="x")
        self.passages_list_tree.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

    def search(self, *args):
        print(f"args: {args}")
        print(f"Searching for {self.search_var.get()}")
        search_text = self.search_bar.get()
        print(f"Searching for {search_text} in passages")
        self.passages_list_tree.delete(*self.passages_list_tree.get_children())
        passages_list = self.parser.passages.get_keys()
        for i, name in enumerate(passages_list):
            if search_text.lower() in name.lower():
                if name in self.parser.script_parser.events:
                    self.passages_list_tree.insert(
                        "",
                        tk.END,
                        values=(i, name, "x")
                    )
                else:
                    self.passages_list_tree.insert(
                        "",
                        tk.END,
                        values=(i, name, "")
                    )
