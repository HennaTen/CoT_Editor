import tkinter as tk
from app.gui.elements.content_text import ContentText
from app.gui.elements.right_click_menu import SexyRightClickMenu

class ContentFrame(tk.Frame):
    def __init__(self, root, parser, left_panel, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)

        self.head_frame = tk.Frame(self)

        self.pid_text = tk.Text(self.head_frame, height=1)
        self.name_text = tk.Text(self.head_frame, height=1)
        self.tag_text = tk.Text(self.head_frame, height=1)
        self.generate_head_frame()

        self.content_frame = tk.Frame(self)
        self.content_text = ContentText(self.content_frame)
        content_scrollbar = tk.Scrollbar(self.content_frame)
        self.content_text.config(yscrollcommand=content_scrollbar.set)
        content_scrollbar.config(command=self.content_text.yview)

        sexy_menu = SexyRightClickMenu(self.content_frame, self.content_text)
        self.content_text.bind("<Button-3>", sexy_menu.click)

        self.content_text.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")

        end_label = tk.Label(self, text="</tw-passagedata>")
        passage_buttons_frame = tk.Frame(self)
        self.escape_button = tk.Button(passage_buttons_frame, text="Copy escaped text",
                                       command=lambda: self.escape(left_panel, parser))
        self.escape_button["state"] = "disabled"
        self.full_escape_button = tk.Button(passage_buttons_frame, text="Copy whole tw-passagedata",
                                            command=lambda: self.escape(left_panel, parser, full=True))
        self.full_escape_button["state"] = "disabled"
        self.escape_button.grid(column=0, row=0)
        self.full_escape_button.grid(column=1, row=0)

        self.head_frame.pack(side="top")
        self.content_frame.pack(side="top", fill="both", expand=True)
        end_label.pack(side="top")
        passage_buttons_frame.pack(side="bottom", fill="x")

    def generate_head_frame(self):
        a = tk.Label(self.head_frame, text="<tw-passagedata pid=")
        b = tk.Label(self.head_frame, text="name=")
        c = tk.Label(self.head_frame, text="tags=")
        d = tk.Label(self.head_frame, text="position=\"{position}\" size=\"{size}\">")

        a.pack()
        self.pid_text.pack()
        b.pack()
        self.name_text.pack()
        c.pack()
        self.tag_text.pack()
        d.pack()

    def escape(self, left_panel, parser, full=None):
        iid = left_panel.passages_list_tree.selection()[0]
        _, selected, is_event = left_panel.passages_list_tree.item(iid)['values']

        text = self.content_text.original_text
        additional_data = None
        if full:
            additional_data = {
                "pid": self.pid_text.get("1.0", tk.END),
                "name": self.name_text.get("1.0", tk.END),
                "tags": self.tag_text.get("1.0", tk.END),
            }
        escaped = parser.passages[selected].escape(text, data=additional_data)
        self.clipboard_clear()
        self.clipboard_append(escaped)

    def update_elements(self, passage):
        self.pid_text.delete(1.0, tk.END)
        self.pid_text.insert(tk.END, passage.pid)
        self.name_text.delete(1.0, tk.END)
        self.name_text.insert(tk.END, passage.name)
        self.tag_text.delete(1.0, tk.END)
        self.tag_text.insert(tk.END, passage.tags)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, passage.content)
        # If translation is enabled, apply it
        if self.content_text.translate_var.get():
            self.content_text.toggle_translation()

        self.escape_button["state"] = "active"
        self.full_escape_button["state"] = "active"