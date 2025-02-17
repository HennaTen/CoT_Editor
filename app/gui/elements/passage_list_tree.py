import tkinter as tk
from tkinter import ttk


class PassageListTree(ttk.Treeview):
    def __init__(self, root, parser):
        columns = ("Id", "Passages", "Is Event")
        ttk.Treeview.__init__(self, root, columns=columns)
        self['show'] = 'headings'
        self.heading("Id", text="Id")
        self.heading("Passages", text="Passages")
        self.heading("Is Event", text="Is Event")
        self.column("Id", width=35)
        self.column("Passages", width=250)
        self.column("Is Event", width=45)

        self.parser = parser
        self.generate_tree()

        for col in columns:
            self.heading(col, text=col,
                             command=lambda c=col: self.sort(c, False))

    def generate_tree(self):
        passages_list = self.parser.passages.get_keys()
        for i, name in enumerate(passages_list):
            if name in self.parser.script_parser.events:
                self.insert(
                    "",
                    tk.END,
                    values=(i, name, "x")
                )
            else:
                self.insert(
                    "",
                    tk.END,
                    values=(i, name, "")
                )

    def sort(self, col, reverse):
        print(f"Sorting {col} in reverse: {reverse}")
        l = [(self.set(k, col), k) for k in self.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        self.heading(col, command=lambda: self.sort(col, not reverse))