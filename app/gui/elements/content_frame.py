import tkinter as tk
from app.gui.elements.content_text import ContentText
from app.gui.elements.right_click_menu import SexyRightClickMenu


class ContentFrame(tk.Frame):
    def __init__(self, root, passages_data, left_panel, **kwargs):
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
        self.generate_buttons_frame(left_panel, passages_data)

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

    def generate_buttons_frame(self, left_panel, passages_data):
        # header_label = tk.Label(self.passage_buttons_frame, text="Show header:")
        # header_checkbox = tk.Checkbutton(self.passage_buttons_frame, variable=self.content_elements["content_text"].show_header_var,
        #                                  command=self.content_elements["content_text"].toggle_header)
        # self.buttons_elements["header_checkbox"] = header_checkbox

        translate_label = tk.Label(self.passage_buttons_frame, text="Translate:")
        translate_checkbox = tk.Checkbutton(self.passage_buttons_frame, variable=self.content_elements["content_text"].translate_var,
                                            command=self.content_elements["content_text"].toggle_translation)
        self.buttons_elements["translate_checkbox"] = translate_checkbox

        self.buttons_elements["escape_button"] = tk.Button(self.passage_buttons_frame, text="Copy escaped text",
                                       command=lambda: self.escape(left_panel, passages_data))
        self.buttons_elements["escape_button"]["state"] = "disabled"
        self.buttons_elements["full_escape_button"] = tk.Button(self.passage_buttons_frame, text="Copy whole tw-passagedata",
                                            command=lambda: self.escape(left_panel, passages_data, full=True))
        self.buttons_elements["full_escape_button"]["state"] = "disabled"

        self.buttons_elements["translate_checkbox"].grid(column=0, row=0)
        self.buttons_elements["escape_button"].grid(column=1, row=0)
        self.buttons_elements["full_escape_button"].grid(column=2, row=0)

    def update_elements(self, passage):
        self.head_elements["pid_text"].delete(0, tk.END)
        self.head_elements["pid_text"].insert(tk.END, passage.pid)
        self.head_elements["name_text"].delete(0, tk.END)
        self.head_elements["name_text"].insert(tk.END, passage.name)
        self.head_elements["tag_text"].delete(0, tk.END)
        self.head_elements["tag_text"].insert(tk.END, passage.tags)
        self.content_elements["content_text"].update_data(self.passages_data[passage.name])
        # self.content_elements["content_text"].delete(1.0, tk.END)
        # self.content_elements["content_text"].insert(tk.END, passage["text"])
        # If translation is enabled, apply it
        if self.content_elements["content_text"].translate_var.get():
            self.content_elements["content_text"].toggle_translation()

        self.buttons_elements["escape_button"]["state"] = "active"
        self.buttons_elements["full_escape_button"]["state"] = "active"

    def escape(self, left_panel, passages_data, full=None):
        iid = left_panel.passages_list_tree.selection()[0]
        _, selected, is_event = left_panel.passages_list_tree.item(iid)['values']

        text = self.content_elements["content_text"].passage_data.text # TODO: use passage_data instead of xxx.xxx.passagge_data
        additional_data = None
        if full:
            additional_data = {
                "pid": self.head_elements["pid_text"].get(),
                "name": self.head_elements["name_text"].get(),
                "tags": self.head_elements["tag_text"].get(),
            }
        escaped = passages_data[selected].escape(data=additional_data)
        self.clipboard_clear()
        self.clipboard_append(escaped)
