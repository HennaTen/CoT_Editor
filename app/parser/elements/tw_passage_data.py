import html


class TWPassageData:
    def __init__(self, pid, name, tags, position, size, content):
        self.pid = pid
        self.name = name
        self.tags = tags.split(" ")
        self.position = position
        self.size = size
        self.content = html.unescape(content)

    def escape(self, text=None, data=None):

        if not text:
            escaped = html.escape(self.content)
        else:
            escaped = html.escape(text)

        if data:
            open_tag = (f'<tw-passagedata pid="{data["pid"].rstrip()}" name="{data["name"].rstrip()}" tags="{data["tags"].rstrip()}" '
                        f'position="{self.position}" size="{self.size}">')
            close_tag = "</tw-passagedata>"
            print(f"{open_tag}{escaped}{close_tag}")
            return f"{open_tag}{escaped}{close_tag}"
        return escaped

    def restore(self):
        open_tag = (f"<tw-passagedata pid=\"{self.pid}\" name=\"{self.name}\" tags=\"{' '.join(self.tags)}\" "
                    f"position=\"{self.position}\" size=\"{self.size}\">")
        content = self.escape()
        close_tag = "</tw-passagedata>"
        return f"{open_tag}{content}{close_tag}"

    def __str__(self):
        return f"name: {self.name}, tags: {self.tags}"

    def __repr__(self):
        return "pid: %s, name: %s, tags: %s, position: %s, size: %s" % (self.pid, self.name, self.tags,
                                                                        self.position, self.size)
