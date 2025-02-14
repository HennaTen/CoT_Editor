import tkinter as tk
from app.data.cot_data import pronoun_tags


class ContentText(tk.Text):
    def __init__(self, root, *args, **kwargs):
        tk.Text.__init__(self, root, *args, **kwargs)
        self.original_text = self.get("1.0", tk.END)
        self.translate_var = tk.BooleanVar()

        self.tag_config("sexy_highlight", background="green")
        self.tag_config("naughty_highlight", background="red")

        self.bind('<<Modified>>', self.on_text_modified)


    def translate_text(self):
        """Translate text by replacing tags with their corresponding values."""
        translated = self.get("1.0", tk.END)
        for tag, replacement in pronoun_tags.items():
            translated = translated.replace(tag, replacement)
        return translated

    def untranslate_text(self):
        """Convert translated text back to tagged format."""
        untranslated = self.get("1.0", tk.END)
        for tag, replacement in pronoun_tags.items():  # TODO; use tk.tag instead of tag
            untranslated = untranslated.replace(replacement, tag)
        return untranslated

    def toggle_translation(self):
        """Handle translation toggle."""
        # Get current cursor position
        current_pos = self.index(tk.INSERT)

        if self.translate_var.get():
            # Show translated text
            # self.apply_tags()  # TODO: remove if
            translated = self.translate_text()
            self.delete('1.0', tk.END)
            self.insert('1.0', translated)
            self.apply_tags()

        else:
            # Show original text
            self.delete('1.0', tk.END)
            self.insert('1.0', self.original_text)

        # Restore cursor position
        self.mark_set(tk.INSERT, current_pos)

    def on_text_modified(self, event):
        """Handle text modifications."""
        if self.edit_modified():
            current_text = self.get('1.0', 'end-1c')

            if not self.translate_var.get():
                # Update original text when editing in untranslated mode
                self.original_text = current_text
            else:
                # Update original text when editing in translated mode
                self.original_text = self.untranslate_text()

            self.edit_modified(False)

    def apply_tags(self):
        for tag, replacement in pronoun_tags.items():
            self.highlight_pattern(replacement, "sexy_highlight")

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

