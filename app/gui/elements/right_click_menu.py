import tkinter as tk
from app.tools.json_convert import convert_dir_to_dict, convert_to_dict, convert_to_json


class Submenu:
    menu_elements = {}

    def __init__(self, root, items):
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=0)
        self.items = items


class InsertsMenu(Submenu):
    def __init__(self, root, items, func):
        Submenu.__init__(self, root, items=items)
        for key in self.items.keys():
            begin_ = self.items[key]["begin"]
            if "end" in self.items[key]:
                begin_ += self.items[key]["end"]
            if "background" in self.items[key]:
                background = self.items[key]["background"]
                self.menu.add_command(label=key, background=background, command=lambda begin=begin_: func(var_=begin_))
            else:
                self.menu.add_command(label=key, command=lambda begin=begin_: func(var_=begin))


class ContainersMenu(Submenu):
    def __init__(self, root, func, items=None, items_dir=None):
        Submenu.__init__(self, root, items=items)

        for key in self.items.keys():
            begin_ = self.items[key]["begin"]
            if "end" in self.items[key]:
                end_ = self.items[key]["end"]
            else:
                end_ = ""
            if "background" in self.items[key]:
                background = self.items[key]["background"]
                print(f"color: {background}")
                self.menu.add_command(label=key, background=background,
                                      command=lambda begin=begin_, end=end_: func(begin, end))
            else:
                print(f"no color: {key}")
                self.menu.add_command(label=key,
                                      command=lambda begin=begin_, end=end_: func(begin, end))


class SexyRightClickMenu:
    def __init__(self, root, content_text):
        self.root = root
        self.content_text = content_text
        self.menu = None
        self.ranges = None
        self.container_submenu = {}
        containers = convert_dir_to_dict("config/containers")
        for item_name in containers.keys():
            items = containers[item_name]
            self.container_submenu[item_name] = ContainersMenu(self.root, items=items, func=self.replace)


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
        for key in self.container_submenu.keys():
            self.menu.add_cascade(label=key, menu=self.container_submenu[key].menu)

    def menu_insert(self, event=None):
        print("menu insert")
        for key in self.insert_submenus.keys():
            self.menu.add_cascade(label=key, menu=self.insert_submenus[key].menu)

    def insert(self, var_=None):
        self.content_text.insert(tk.INSERT, var_)

    def replace(self, begin, end):
        ranges = self.content_text.tag_ranges(tk.SEL)
        selection = self.content_text.get(*self.ranges)
        self.content_text.replace(*ranges, f"{begin}{selection}{end}")