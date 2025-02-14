import tkinter as tk
from app.data.cot_data import pronoun_female, pronoun_male, pronoun_nonbinary
from app.gui.elements.content_text import ContentText
from app.gui.elements.right_click_menu import SexyRightClickMenu

class PassageFrame:
    def __init__(self, root, parser):
        self.frame = tk.Frame(root)
        self.parser = parser
        self.elements = {}
        self.edited = False

        self.setup_passages()
        self.frame.pack(fill='both', expand=True)

    def setup_passages(self):  # TODO: Reorganize THAT
        left_panel = tk.Frame(self.frame, relief=tk.GROOVE)
        middle_panel = tk.Frame(self.frame, relief=tk.GROOVE)
        right_panel = tk.Frame(self.frame, relief=tk.GROOVE)

        # LEFT
        passages_listbox = tk.Listbox(left_panel, width=50, exportselection=False)

        def generate_passages_listbox(order=None):
            bak_value = None
            if passages_listbox.curselection():
                index = passages_listbox.curselection()[0]
                bak_value = passages_listbox.get(index)

            passages_listbox.delete(0, 'end')
            passages_list = self.parser.passages.get_keys()
            if order == "alpha":
                passages_list.sort()
            for i, name in enumerate(passages_list):
                if name in self.parser.script_parser.events:
                    passages_listbox.insert(i, name + " ---EVENT")
                else:
                    passages_listbox.insert(i, name)

            if bak_value:
                new_index = passages_listbox.get(0, "end").index(bak_value)
                print(f"index {new_index} for {passages_listbox.get(new_index)}")
                passages_listbox.selection_set(new_index)

        generate_passages_listbox()

        def selection_changed(event_):
            index = int(passages_listbox.curselection()[0])
            value = passages_listbox.get(index)
            selected = value.split(" ")[0]
            print(selected)
            passage = self.parser.passages[selected]
            pid_text.delete(1.0, tk.END)
            pid_text.insert(tk.END, passage.pid)
            name_text.delete(1.0, tk.END)
            name_text.insert(tk.END, passage.name)
            tag_text.delete(1.0, tk.END)
            tag_text.insert(tk.END, passage.tags)
            content_text.delete(1.0, tk.END)
            content_text.insert(tk.END, passage.content)

            event_passage.config(text="")
            event_tags.delete(1.0, tk.END)
            event_frequency.delete(1.0, tk.END)
            event_additional_tags.delete(1.0, tk.END)
            if selected in self.parser.script_parser.events:
                event_passage.config(text=self.parser.script_parser.events[selected].passage)
                event_tags.insert(tk.END, self.parser.script_parser.events[selected].tags)
                event_frequency.insert(tk.END, self.parser.script_parser.events[selected].frequency)
                event_additional_tags.insert(tk.END, self.parser.script_parser.events[selected].additional_tags)
            escape_button["state"] = "active"
            full_escape_button["state"] = "active"

        passages_listbox.bind("<<ListboxSelect>>", selection_changed)

        scrollbar = tk.Scrollbar(left_panel)
        passages_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=passages_listbox.yview)

        passages_list_buttons = tk.Frame(left_panel)
        natural_order_button = tk.Button(passages_list_buttons, text="Normal order", command=generate_passages_listbox)
        alpha_order_button = tk.Button(passages_list_buttons,
                                       text="Alphabetical order", command=lambda: generate_passages_listbox("alpha"))

        natural_order_button.pack(side="left")
        alpha_order_button.pack(side="left")
        passages_list_buttons.pack(side="bottom", fill="x")
        passages_listbox.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")
        # END_LEFT

        # MIDDLE
        head_frame = tk.Frame(middle_panel)

        pid_text = tk.Text(head_frame, height=1)
        name_text = tk.Text(head_frame, height=1)
        tag_text = tk.Text(head_frame, height=1)

        def generate_head_frame():
            a = tk.Label(head_frame, text="<tw-passagedata pid=")
            b = tk.Label(head_frame, text="name=")
            c = tk.Label(head_frame, text="tags=")
            d = tk.Label(head_frame, text="position=\"{position}\" size=\"{size}\">")

            a.pack()
            pid_text.pack()
            b.pack()
            name_text.pack()
            c.pack()
            tag_text.pack()
            d.pack()

        generate_head_frame()

        content_frame = tk.Frame(middle_panel)
        content_text = ContentText(content_frame)
        content_scrollbar = tk.Scrollbar(content_frame)
        content_text.config(yscrollcommand=content_scrollbar.set)
        content_scrollbar.config(command=content_text.yview)

        # def test_insert(event_=None, var_=None):
        #     content_text.insert(tk.INSERT, var_)
        #
        # def test_replace(event_=None, var_=None):
        #     content_text.insert(tk.INSERT, var_)
        #
        # def test_menu(event_=None):
        #     print("right click")
        #     m = tk.Menu(self.frame, tearoff=0)
        #     ranges = content_text.tag_ranges(tk.SEL)
        #     if ranges:
        #         test = content_text.get(*ranges)
        #         print(f'SELECTED Text is {test} in range {ranges}')
        #         if test in pronoun_female.keys():
        #             m.add_command(label=f"{test}", background="lightblue")
        #             m.add_command(label=f"{pronoun_female[test]}")
        #             m.add_command(label=f"{pronoun_male[test]}")
        #             m.add_command(label=f"{pronoun_nonbinary[test]}")
        #         # elif test in test_tags.keys():
        #         #     m.add_command(label=f"{test_tags[test]}")
        #         #     m.add_command(label=f"{test}", background="lightblue")
        #         # m.add_separator()
        #         # m.add_command(label="Replace selection menu here")
        #         # m.add_separator()
        #         # m.add_command(label="Info")
        #     else:
        #         print('NO Selected Text')
        #         m.add_command(label="Insert test", command=lambda: test_insert(var_="Test"))
        #         m.add_separator()
        #         m.add_command(label="Insert menu here")
        #         m.add_command(label="Like Link/skillgates")
        #     try:
        #         m.tk_popup(event_.x_root, event_.y_root)
        #     finally:
        #         m.grab_release()


        sexy_menu = SexyRightClickMenu(self.frame, content_text)
        content_text.bind("<Button-3>", sexy_menu.click)

        content_text.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")

        def escape(full=None):
            index = int(passages_listbox.curselection()[0])
            value = passages_listbox.get(index)
            selected = value.split(" ")[0]
            text = content_text.get("1.0", tk.END)
            additional_data = None
            if full:
                additional_data = {
                    "pid": pid_text.get("1.0",tk.END),
                    "name": name_text.get("1.0",tk.END),
                    "tags": tag_text.get("1.0",tk.END),
                }
            escaped = self.parser.passages[selected].escape(text, data=additional_data)
            self.frame.clipboard_clear()
            self.frame.clipboard_append(escaped)

        end_label = tk.Label(middle_panel, text="</tw-passagedata>")
        passage_buttons_frame = tk.Frame(middle_panel)
        escape_button = tk.Button(passage_buttons_frame, text="Copy escaped text", command=escape)
        escape_button["state"] = "disabled"
        full_escape_button = tk.Button(passage_buttons_frame, text="Copy whole tw-passagedata",
                                       command=lambda: escape(full=True))
        full_escape_button["state"] = "disabled"
        escape_button.grid(column=0, row=0)
        full_escape_button.grid(column=1, row=0)

        head_frame.pack(side="top")
        content_frame.pack(side="top", fill="both", expand=True)
        end_label.pack(side="top")
        passage_buttons_frame.pack(side="bottom", fill="x")
        # END_MIDDLE

        # RIGHT
        event = tk.Label(right_panel, text="Event: ")
        event_passage = tk.Label(right_panel)
        event_tags = tk.Text(right_panel, height=1, width=60)
        event_frequency = tk.Text(right_panel, height=1, width=60)
        event_additional_tags = tk.Text(right_panel, width=60)

        event.pack()
        event_passage.pack()
        event_tags.pack()
        event_frequency.pack()
        event_additional_tags.pack()
        # END_RIGHT

        left_panel.pack(side='left',  fill='y',  padx=10,  pady=5,  expand=True)
        middle_panel.pack(side="left", fill='both', expand=True)
        right_panel.pack(side="left", fill='y', expand=True)