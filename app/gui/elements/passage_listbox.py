import tkinter as tk

class PassageListbox(tk.Listbox):
    def __init__(self, root, parser):
        tk.Listbox.__init__(self, root, width=50, exportselection=False)
        self.parser = parser
        self.generate_passages_listbox()

    def generate_passages_listbox(self, order=None):
        bak_value = None
        if self.curselection():
            index = self.curselection()[0]
            bak_value = self.get(index)

        self.delete(0, 'end')
        passages_list = self.parser.passages.get_keys()
        if order == "alpha":
            passages_list.sort()
        for i, name in enumerate(passages_list):
            if name in self.parser.script_parser.events:
                self.insert(i, name + " ---EVENT")
            else:
                self.insert(i, name)

        if bak_value:
            new_index = self.get(0, "end").index(bak_value)
            self.selection_set(new_index)