import tkinter as tk
import html

class ContentData:
    def __init__(self, pid, name, tags, text, event=None, position="0", size="100,100"):
        self.original = {
            "pid": pid,
            "name": name,
            "tags": " ".join(tags),
            "text": text,
            "position": position,
            "size": size,
            "event": event
        }

        self.pid = tk.StringVar(value=pid)
        self.name = tk.StringVar(value=name)
        self.tags = tk.StringVar(value=" ".join(tags))
        self.text = text
        self.event = event

    def get_header(self):
        return (f'<tw-passagedata pid="{self.pid.get()}" name="{self.name.get()}" tags="{self.tags.get()}" '
                f'position="{self.original["position"]}" size="{self.original["size"]}">')

    @classmethod
    def get_footer(cls):
        return "</tw-passagedata>"

    # def get_passage_data(self): # TODO use this if tkinter vars are used
    #     return {
    #         "pid": self.pid.get(),
    #         "name": self.name.get(),
    #         "tags": self.tags.get(),
    #         "text": self.text.get(),
    #         "position": self.original["position"],
    #         "size": self.original["size"],
    #         "event": self.event
    #     }

    def escape(self, data=False):
        escaped = html.escape(self.text)
        if data:
            open_tag = self.get_header()
            close_tag = self.get_footer()
            print(f"{open_tag}{escaped}{close_tag}")
            return f"{open_tag}{escaped}{close_tag}"
        return escaped