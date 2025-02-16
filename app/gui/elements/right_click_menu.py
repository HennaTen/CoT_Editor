import tkinter as tk

def rgb(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

class AbstractSubmenu:
    menu_elements = {}

    def __init__(self, root, selected):
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=0)
        self.selected = None
        # self.update(selected)


    def update(self, selected, ranges, content_text):
        self.selected = selected


class MenuColorEffect(AbstractSubmenu):
    color_classes = {
        "sexy": rgb(196, 76, 142),
        "romantic":  rgb(245, 65, 89),
        "festive":  rgb(202, 58, 94),
        "gold":  rgb(216, 219, 29), # Not used as <<highlight>> ?
        "mainskill":  rgb(179, 40, 116),
        "otherskill":  rgb(119, 191, 224),
        "decreaseneed":  rgb(194, 51, 32),
        "increaseneed":  rgb(57, 160, 26),
        "equalneed":  rgb(102, 108, 109),
        "pee":  rgb(221, 209, 101),
        "cash":  rgb(58, 148, 66),
        "notice":  rgb(108, 208, 226),
        "noticedark":  rgb(66, 131, 143),
        "bad":  rgb(190, 10, 10),
        "ungood":  rgb(187, 190, 10),
        "unbad":  rgb(118, 226, 108),
        "female":  rgb(255, 0, 255),
        "male": rgb(0, 0, 255),
        "nonbinary":  rgb(0, 255, 255),
        "glow":  "#fff",
    }

    def __init__(self, root, selected):
        AbstractSubmenu.__init__(self, root, selected)

    def update(self, selected, ranges, content_text, event=None):
        self.selected = selected
        self.menu.delete(0, tk.END)
        for key in self.color_classes.keys():

            def replace(color_name):
                content_text.replace(*ranges, f"<<highlight {color_name}>>{self.selected}<</highlight>>")

            color = self.color_classes[key]
            self.menu.add_command(label=key, background=color, command=lambda x=key: replace(x))



class SexyRightClickMenu:
    def __init__(self, root, content_text):
        self.root = root
        self.content_text = content_text
        self.menu = None
        self.selection = None
        self.ranges = None
        self.submenu = {
            "color": MenuColorEffect(self.root, self.selection)
        }

    def click(self, event=None):
        print("right click")
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_checkbutton(label="Translate", onvalue=True, offvalue=False, variable=self.content_text.translate_var, command=lambda: self.content_text.toggle_translation())
        self.menu.add_separator()
        self.ranges = self.content_text.tag_ranges(tk.SEL)

        if self.ranges:
            self.selection = self.content_text.get(*self.ranges)
            print(f'SELECTED Text is {self.selection} in range {self.ranges}')
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

        self.menu.add_cascade(label="<<highlight>>", menu=self.submenu["color"].menu)

        self.menu.add_command(label=f"It will have other options to apply tags to {self.selection} here")
        # if self.selection in pronoun_tags.keys():
        #     self.menu.add_command(label=f"{self.selection}", background="lightblue")
        #     self.menu.add_command(label=f"{pronoun_tags[self.selection]}")
        # elif self.selection in pronoun_tags.keys():
        #     self.menu.add_command(label=f"{pronoun_tags[self.selection]}")
        #     self.menu.add_command(label=f"{self.selection}", background="lightblue")
        # self.menu.add_separator()
        # self.menu.add_command(label="Replace selection menu here")
        #
        # self.menu.add_separator()
        # self.menu.add_command(label="Info")

    def menu_insert(self, event=None):
        print("menu insert")
        self.menu.add_command(label="It will have options to insert elements here")  # , command=lambda: self.test_insert(var_="Test"))
        #self.menu.add_separator()
        # self.menu.add_command(label="Insert menu here")
        # self.menu.add_command(label="Like Link/skillgates")

    def update_submenus(self):
        for key in self.submenu.keys():
            self.submenu[key].update(self.selection, self.ranges, self.content_text)

    def test_insert(self, event_=None, var_=None):
        self.content_text.insert(tk.INSERT, var_)

    def test_replace(self, event_=None, var_=None):
        self.content_text.insert(tk.INSERT, var_)