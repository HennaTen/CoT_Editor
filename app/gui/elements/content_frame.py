import tkinter as tk
from app.gui.elements.content_text import ContentText
from app.gui.elements.right_click_menu import SexyRightClickMenu


class ContentFrame(tk.Frame):
    def __init__(self, root, passages_data, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.passages_data = passages_data

        self.head_frame = tk.Frame(self)
        self.head_elements = {}
        self.generate_head_frame()

        self.content_frame = tk.Frame(self)
        self.content_elements = {}
        self.generate_content_frame()

        self.passage_buttons_frame = tk.Frame(self)
        self.buttons_elements = {}
        self.generate_buttons_frame()

        self.head_frame.pack(side="top")
        self.content_frame.pack(side="top", fill="both", expand=True)
        self.passage_buttons_frame.pack(side="bottom", fill="x")

        sexy_menu = SexyRightClickMenu(self.content_frame, self.content_elements["content_text"])
        self.content_elements["content_text"].bind("<Button-3>", sexy_menu.click)

    def generate_head_frame(self):
        pid_label = tk.Label(self.head_frame, text="pid:")
        name_label = tk.Label(self.head_frame, text="name:")
        tags_label = tk.Label(self.head_frame, text="tags:")

        self.head_elements["pid_text"] = tk.Entry(self.head_frame, width=70)
        self.head_elements["name_text"] = tk.Entry(self.head_frame, width=70)
        self.head_elements["tag_text"] = tk.Entry(self.head_frame, width=70)

        pid_label.grid(row=0, column=0)
        self.head_elements["pid_text"].grid(row=0, column=1)
        name_label.grid(row=1, column=0)
        self.head_elements["name_text"].grid(row=1, column=1)
        tags_label.grid(row=2, column=0)
        self.head_elements["tag_text"].grid(row=2, column=1)

    def generate_content_frame(self):
        self.content_elements["content_text"] = ContentText(self.content_frame, passage_data=None)
        content_scrollbar = tk.Scrollbar(self.content_frame)
        self.content_elements["content_text"].config(yscrollcommand=content_scrollbar.set)
        content_scrollbar.config(command=self.content_elements["content_text"].yview)

        self.content_elements["content_text"].pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")

    def generate_buttons_frame(self):
        translate_label = tk.Label(self.passage_buttons_frame, text="Translate:")
        translate_checkbox = tk.Checkbutton(self.passage_buttons_frame, variable=self.content_elements["content_text"].translate_var,
                                            command=self.content_elements["content_text"].toggle_translation)
        self.buttons_elements["translate_checkbox"] = translate_checkbox

        self.buttons_elements["reset_button"] = tk.Button(self.passage_buttons_frame, text="Reset to original",
                                 command=self.reset_to_original)
        # Todo: Implement show original or make tabs work (tabs probably better)
        # show_original_label = tk.Label(self.passage_buttons_frame, text="Show original:")
        # show_original_checkbox = tk.Checkbutton(self.passage_buttons_frame, variable=self.content_elements["content_text"].show_original_var,
        #                                     command=self.content_elements["content_text"].toggle_original)

        self.buttons_elements["unescape_button"] = tk.Button(self.passage_buttons_frame, text="Unescape (Human)",
                                       command=lambda: self.content_elements["content_text"].unescape())
        self.buttons_elements["escape_button"] = tk.Button(self.passage_buttons_frame, text="Escape",
                                       command=lambda: self.content_elements["content_text"].escape())

        self.buttons_elements["add_tw_tags_button"] = tk.Button(self.passage_buttons_frame,
                                                                text="Add tw-passagedata tags",
                                                                command=lambda: self.content_elements[
                                                                    "content_text"].add_tw_tags())

        self.buttons_elements["remove_tw_tags_button"] = tk.Button(self.passage_buttons_frame,
                                                                text="Remove tw-passagedata tags",
                                                                command=lambda: self.content_elements[
                                                                    "content_text"].remove_tw_tags())

        self.buttons_elements["undo_button"] = tk.Button(self.passage_buttons_frame, text="Undo",
                                       command=lambda: self.content_elements["content_text"].undo())
        self.buttons_elements["redo_button"] = tk.Button(self.passage_buttons_frame, text="Redo",
                                       command=lambda: self.content_elements["content_text"].redo())

        translate_label.grid(column=0, row=0)
        self.buttons_elements["translate_checkbox"].grid(column=1, row=0)
        self.buttons_elements["reset_button"].grid(column=2, row=0)
        # show_original_label.grid(column=2, row=0)
        # show_original_checkbox.grid(column=3, row=0)
        self.buttons_elements["unescape_button"].grid(column=0, row=1)
        self.buttons_elements["escape_button"].grid(column=1, row=1)
        self.buttons_elements["add_tw_tags_button"].grid(column=3, row=1)
        self.buttons_elements["remove_tw_tags_button"].grid(column=4, row=1)
        self.buttons_elements["undo_button"].grid(column=6, row=1)
        self.buttons_elements["redo_button"].grid(column=7, row=1)

    def update_elements(self, passage):
        self.head_elements["pid_text"].config(textvariable=passage.pid)
        self.head_elements["name_text"].config(textvariable=passage.name)
        self.head_elements["tag_text"].config(textvariable=passage.tags)
        self.content_elements["content_text"].update_data(passage)

        if self.content_elements["content_text"].translate_var.get():
            self.content_elements["content_text"].toggle_translation()

    def reset_to_original(self):
        self.head_elements["pid_text"].delete(0, tk.END)
        self.head_elements["pid_text"].insert(tk.END, self.content_elements["content_text"].passage_data.original["pid"])
        self.head_elements["name_text"].delete(0, tk.END)
        self.head_elements["name_text"].insert(tk.END, self.content_elements["content_text"].passage_data.original["name"])
        self.head_elements["tag_text"].delete(0, tk.END)
        self.head_elements["tag_text"].insert(tk.END, self.content_elements["content_text"].passage_data.original["tags"])
        self.content_elements["content_text"].delete(1.0, tk.END)
        self.content_elements["content_text"].insert(tk.END, self.content_elements["content_text"].passage_data.original["text"])

