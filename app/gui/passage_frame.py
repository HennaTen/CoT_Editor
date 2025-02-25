import tkinter as tk
from app.gui.elements.event_frame import EventFrame
from app.gui.elements.passage_list_frame import PassageListFrame
from app.gui.elements.content_frame import ContentFrame
# from app.parser.elements.content_data import ContentData

class PassageFrame:
    def __init__(self, root, passages_data):
        self.frame = tk.Frame(root)
        self.passages_data = passages_data

        self.passage_list_frame = PassageListFrame(self.frame, self.passages_data, relief=tk.GROOVE)
        self.content_frame = ContentFrame(self.frame, self.passages_data)
        self.event_frame = EventFrame(self.frame)

        self.setup_passages()
        self.frame.pack(fill='both', expand=True)

    def setup_passages(self):
        self.passage_list_frame.passages_list_tree.bind("<<TreeviewSelect>>", self.selection_changed)

        self.passage_list_frame.pack(side='left', fill='y', padx=10, pady=5, expand=True)
        self.content_frame.pack(side="left", fill='both', expand=True)
        self.event_frame.pack(side="left", fill='y', expand=True)

    def selection_changed(self, event):
        iid = self.passage_list_frame.passages_list_tree.selection()[0]
        _, selected, is_event = self.passage_list_frame.passages_list_tree.item(iid)['values']

        passage = self.passages_data[selected]
        print(f"Selected passage: {passage}")
        print(f"pid: {passage.pid}")
        self.content_frame.update_elements(passage)
        # if is_event:
        self.event_frame.update_event_data(passage.event)
        # else:
        #     self.event_frame.update_event_data(None)

