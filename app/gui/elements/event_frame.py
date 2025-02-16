import tkinter as tk

class EventFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # Create frame content
        self.event = tk.Label(self, text="Event: ")
        self.event_passage = tk.Label(self)
        self.event_tags = tk.Text(self, height=1, width=60)
        self.event_frequency = tk.Text(self, height=1, width=60)
        self.event_additional_tags = tk.Text(self, width=60)

        # Pack widgets
        self.event.pack()
        self.event_passage.pack()
        self.event_tags.pack()
        self.event_frequency.pack()
        self.event_additional_tags.pack()

    def update_event_data(self, event_data):
        if not event_data:
            self.event_passage.config(text="")
            self.event_tags.delete(1.0, tk.END)
            self.event_frequency.delete(1.0, tk.END)
            self.event_additional_tags.delete(1.0, tk.END)
            return
        self.event_passage.config(text=event_data.passage)
        self.event_tags.delete(1.0, tk.END)
        self.event_tags.insert(tk.END, event_data.tags)
        self.event_frequency.delete(1.0, tk.END)
        self.event_frequency.insert(tk.END, event_data.frequency)
        self.event_additional_tags.delete(1.0, tk.END)
        self.event_additional_tags.insert(tk.END, event_data.additional_tags)