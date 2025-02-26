import tkinter as tk
from html import unescape, escape
import re
from app.tools.json_convert import convert_dir_to_dict

key_to_ignore = ["Control_L", "Control_R", "z", "y"]

class ContentText(tk.Text):
    # TODO: Add readonly "source" text. something that would show the original text in another tab
    # TODO: Add a "restore to source" button
    # TODO: Save changes to the original text (cache? File?)
    def __init__(self, root, passage_data, *args, **kwargs):
        tk.Text.__init__(self, root, *args, **kwargs, wrap="word")
        self.passage_data = passage_data
        # self.original_text = self.get("1.0", tk.END)
        self.translate_var = tk.BooleanVar()
        self.show_original_var = tk.BooleanVar()
        self.imported_tags = convert_dir_to_dict("config/translators")

        self.tag_config("sexy_highlight", background="lightblue")
        self.tag_config("naughty_highlight", background="red")

        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind('<<Modified>>', self.on_text_modified)

    def update_data(self, passage_data):
        self.passage_data = passage_data
        self.delete('1.0', tk.END)
        self.insert('1.0', self.passage_data.text)
        if self.translate_var.get():
            self.apply_tags()

    def translate_text(self):
        """Translate text by replacing tags with their corresponding values."""
        translated = self.get("1.0", tk.END)
        for tags in self.imported_tags.values():
            for tag, replacement in tags.items():
                translated = translated.replace(tag, replacement)
        return translated

    def untranslate_text(self):
        """Convert translated text back to tagged format."""
        untranslated = self.get("1.0", tk.END)
        for tags in self.imported_tags.values():
            for tag, replacement in tags.items(): # TODO: use tk.tag instead of tag
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
            self.insert('1.0', self.passage_data.text)

        # Restore cursor position
        self.mark_set(tk.INSERT, current_pos)


    def on_text_modified(self, event):
        """Handle text modifications."""
        if self.edit_modified():
            self.passage_data.undo_stack.append(self.get("1.0", "end-1c"))
            self.passage_data.redo_stack.clear()

            current_text = self.get('1.0', 'end-1c')
            if not self.translate_var.get():
                # Update original text when editing in untranslated mode
                self.passage_data.text = current_text
            else:
                # Update original text when editing in translated mode
                self.passage_data.text = self.untranslate_text()

            self.edit_modified(False)

    def apply_tags(self):
        for tags in self.imported_tags.values():
            for tag, replacement in tags.items():
                print(f"Applying tag: {tag} -> {replacement}")
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
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def transform_passage_content(self, transformation_function):
        # Pattern to match tw-passagedata tags and capture the content
        pattern = r"(<tw-passagedata[^>]*>)(.*?)(</tw-passagedata>)"

        if re.search(pattern, self.passage_data.text, flags=re.DOTALL):
            def replace_function(match):
                opening_tag = match.group(1)
                content = match.group(2)
                closing_tag = match.group(3)
                print(f"opening_tag: {opening_tag}")
                print(f"content: {content}")
                print(f"closing_tag: {closing_tag}")

                transformed_content = transformation_function(content)

                return f"{opening_tag}{transformed_content}{closing_tag}"

            new_text = re.sub(pattern, replace_function, self.passage_data.text, flags=re.DOTALL)
            print(f"new_text: {new_text}")
        else:
            new_text = transformation_function(self.passage_data.text)
        print(f"new_text: {new_text}")
        self.delete("1.0", tk.END)
        self.insert("1.0", new_text)

    def transform_content(self, transformation_function):
        self.delete("1.0", tk.END)
        self.insert("1.0", transformation_function(self.passage_data.text))

    def unescape(self):
        self.transform_passage_content(unescape)

    def escape(self):
        self.transform_passage_content(escape)

    def add_tw_tags(self):
        if not re.search(r"<tw-passagedata[^>]*>", self.passage_data.text):
            self.transform_content(lambda content: f"{self.passage_data.get_header()}{content}{self.passage_data.get_footer()}")

    def remove_tw_tags(self):
        self.transform_content(lambda content: re.sub(r"<tw-passagedata[^>]*>|</tw-passagedata>", "", content))

    def undo(self, event=None):
        if self.passage_data.undo_stack:
            if len(self.passage_data.redo_stack) == 0:
                self.passage_data.undo_stack.pop()
            text = self.passage_data.undo_stack.pop()
            self.passage_data.redo_stack.append(self.get("1.0", "end-1c"))
            self.delete("1.0", tk.END)
            self.insert("1.0", text)
            self.edit_modified(False)

    def redo(self, event=None):
        if self.passage_data.redo_stack:
            text = self.passage_data.redo_stack.pop()
            self.passage_data.undo_stack.append(self.get("1.0", "end-1c"))
            self.delete("1.0", tk.END)
            self.insert("1.0", text)
            self.edit_modified(False)

    # Todo: Make it work as a toggle
    # def show_original_text(self):
    #     original_data = self.passage_data.original["text"]
    #     self.delete("1.0", tk.END)
    #     self.insert("1.0", original_data)
    #     # Disable editing
    #     self.config(state=tk.DISABLED)
    #
    # def show_edited_text(self):
    #     self.delete("1.0", tk.END)
    #     self.insert("1.0", self.passage_data.text)
    #     # Enable editing
    #     self.config(state=tk.NORMAL)
    #
    # def toggle_original(self):
    #     if self.show_original_var.get():
    #         self.show_original_text()
    #     else:
    #         self.show_edited_text()