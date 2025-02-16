import tkinter as tk
from app.gui.elements.event_frame import EventFrame
from app.gui.elements.passage_list_frame import PassageListFrame
from app.gui.elements.content_frame import ContentFrame


class PassageFrame:
    def __init__(self, root, parser):
        self.frame = tk.Frame(root)
        self.parser = parser
        self.elements = {}
        self.edited = False

        self.passage_list_frame = PassageListFrame(self.frame, self.parser, relief=tk.GROOVE)
        self.content_frame = ContentFrame(self.frame, self.parser, self.passage_list_frame)
        self.event_frame = EventFrame(self.frame)

        self.setup_passages()
        self.frame.pack(fill='both', expand=True)

    def setup_passages(self):  # TODO: Reorganize THAT
        self.passage_list_frame.passages_listbox.bind("<<ListboxSelect>>", self.selection_changed)

        self.passage_list_frame.pack(side='left', fill='y', padx=10, pady=5, expand=True)
        self.content_frame.pack(side="left", fill='both', expand=True)
        self.event_frame.pack(side="left", fill='y', expand=True)

    def selection_changed(self, event_):
        index = int(self.passage_list_frame.passages_listbox.curselection()[0])
        value = self.passage_list_frame.passages_listbox.get(index)
        selected = value.split(" ")[0]
        print(selected)
        passage = self.parser.passages[selected]

        self.content_frame.update_elements(passage)
        if selected in self.parser.script_parser.events:
            self.event_frame.update_event_data(self.parser.script_parser.events[selected])
        else:
            self.event_frame.update_event_data(None)

