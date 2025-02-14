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
        for tag, replacement in pronoun_tags.items():
            untranslated = untranslated.replace(replacement, tag)
        return untranslated

    def toggle_translation(self):
        """Handle translation toggle."""
        # Get current cursor position
        current_pos = self.index(tk.INSERT)

        if self.translate_var.get():
            # Show translated text
            translated = self.translate_text()
            self.delete('1.0', tk.END)
            self.insert('1.0', translated)
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