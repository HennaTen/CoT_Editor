import tkinter as tk
from app.data.cot_data import pronoun_tags


class AbstractSubmenu:
    menu_elements = {}

    def __init__(self, root, selected):
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=0)
        self.selected = selected

    def update(self, selected):
        self.selected = selected


class MenuColorEffect(AbstractSubmenu):
    menu_elements = {
        "lightblue": ("lightblue <<tag ", ">>"),
        "lightgreen": ("lightgreen <<tag ", ">>"),
        "lightyellow": ("lightyellow <<tag ", ">>"),
        "red": ("red <<tag ", ">>"),
        "green": ("green <<tag ", ">>"),
    }

    def __init__(self, root, selected):
        AbstractSubmenu.__init__(self, root, selected)
        for key in self.menu_elements.keys():
            value = self.menu_elements[key]
            self.menu.add_command(label=f"{value[0]}{self.selected}{value[1]}", background=key)

    def update(self, selected, event=None):
        self.selected = selected
        self.menu.delete(0, tk.END)
        for key in self.menu_elements.keys():
            value = self.menu_elements[key]
            self.menu.add_command(label=f"{value[0]}{self.selected}{value[1]}", background=key)


class SexyRightClickMenu:
    def __init__(self, root, content_text):
        self.root = root
        self.content_text = content_text
        self.menu = None
        self.selection = None
        self.submenu = {
            "color": MenuColorEffect(self.root, self.selection)
        }

    def click(self, event=None):
        print("right click")
        # self.content_text.test()
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_checkbutton(label="Translate", onvalue=True, offvalue=False, variable=self.content_text.translate_var, command=lambda: self.content_text.toggle_translation())
        ranges = self.content_text.tag_ranges(tk.SEL)

        if ranges:
            self.selection = self.content_text.get(*ranges)
            print(f'SELECTED Text is {self.selection} in range {ranges}')
            self.menu_selection()
        else:
            print('NO Selected Text')
            self.menu_insert()
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
            self.menu = None
            self.selection = None

    def menu_selection(self, event=None):
        print("menu selection")
        self.update_submenus()

        if self.selection in pronoun_tags.keys():
            self.menu.add_command(label=f"{self.selection}", background="lightblue")
            self.menu.add_command(label=f"{pronoun_tags[self.selection]}")
        elif self.selection in pronoun_tags.keys():
            self.menu.add_command(label=f"{pronoun_tags[self.selection]}")
            self.menu.add_command(label=f"{self.selection}", background="lightblue")
        self.menu.add_separator()
        self.menu.add_command(label="Replace selection menu here")
        self.menu.add_cascade(label="Color", menu=self.submenu["color"].menu)

        self.menu.add_separator()
        self.menu.add_command(label="Info")

    def menu_insert(self, event=None):
        print("menu insert")
        self.menu.add_command(label="Insert test", command=lambda: self.test_insert(var_="Test"))
        self.menu.add_separator()
        self.menu.add_command(label="Insert menu here")
        self.menu.add_command(label="Like Link/skillgates")

    def update_submenus(self):
        for key in self.submenu.keys():
            self.submenu[key].update(self.selection)

    def test_insert(self, event_=None, var_=None):
        self.content_text.insert(tk.INSERT, var_)

    def test_replace(self, event_=None, var_=None):
        self.content_text.insert(tk.INSERT, var_)