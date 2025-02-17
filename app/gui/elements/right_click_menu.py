import tkinter as tk
from app.tools.json_convert import convert_dir_to_dict, convert_to_dict, convert_to_json


class Submenu:
    menu_elements = {}

    def __init__(self, root, items=None, items_dir=None):
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=0)
        self.items = items

        if items_dir:
            try:
                print(f"Using {items_dir}")
                self.items = convert_to_dict(items_dir)
            except FileNotFoundError:
                print(f"Error loading {items_dir}")


class InsertsMenu(Submenu):
    def __init__(self, root, items, func):
        Submenu.__init__(self, root, items=items)
        for key in self.items.keys():
            self.menu.add_command(label=key, command=lambda x=self.items[key]: func(var_=x))


class MenuColorEffect(Submenu):
    def __init__(self, root, func, items=None, items_dir=None):
        Submenu.__init__(self, root, items_dir=items_dir)
        if not self.items:
            from app.data.cot_data import color_classes
            self.items = color_classes
            print("Using color_classes from cot_data")

        begin = "<<highlight "
        middle = ">>"
        end = "<</highlight>>"
        for key in self.items.keys():
            color = self.items[key]
            self.menu.add_command(label=key, background=color, command=lambda x=key: func(x, begin, middle, end))


class SexyRightClickMenu:
    def __init__(self, root, content_text):
        self.root = root
        self.content_text = content_text
        self.menu = None
        self.ranges = None
        self.replace_submenu = {
            "color": MenuColorEffect(self.root, items_dir="config/containers/highlight.json", func=self.replace),
        }

        self.insert_submenus = {}
        inserts = convert_dir_to_dict("config/inserts")
        for item_name in inserts.keys():
            items = inserts[item_name]
            self.insert_submenus[item_name] = InsertsMenu(self.root, items=items, func=self.insert)


    def click(self, event=None):
        print("right click")
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_checkbutton(label="Translate", onvalue=True, offvalue=False, variable=self.content_text.translate_var, command=lambda: self.content_text.toggle_translation())
        self.menu.add_separator()
        self.ranges = self.content_text.tag_ranges(tk.SEL)

        if self.ranges:
            self.menu_selection()
        else:
            self.menu_insert()
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
            self.menu = None

    def menu_selection(self, event=None):
        print("menu selection")
        for key in self.replace_submenu.keys():
            self.menu.add_cascade(label=key, menu=self.replace_submenu[key].menu)

    def menu_insert(self, event=None):
        print("menu insert")
        for key in self.insert_submenus.keys():
            self.menu.add_cascade(label=key, menu=self.insert_submenus[key].menu)

    def insert(self, var_=None):
        self.content_text.insert(tk.INSERT, var_)

    def replace(self, var_, begin="<<", middle= "", end=">>"):
        ranges = self.content_text.tag_ranges(tk.SEL)
        selection = self.content_text.get(*self.ranges)
        self.content_text.replace(*ranges, f"{begin}{var_}{middle}{selection}{end}")