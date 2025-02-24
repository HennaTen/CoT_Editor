from bs4 import BeautifulSoup
from app.parser.tw_passage_data_manager import TWPassageDataManager
from app.parser.tw_user_script_parser import TWUserScriptParser
from app.parser.elements.content_data import ContentData


class CoTParser:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as file:
            # Read the file content
            html_content = file.read()

            # Parse the HTML content using BeautifulSoup
            self.soup = BeautifulSoup(html_content, 'html.parser')

            # Parse the Twine user script
            self.script_parser = TWUserScriptParser(self.soup)

            # Get all passages into custom class
            self.passages = TWPassageDataManager(self.soup) # TODO: Redundant, remove need to remove this at some point

            # Generate passages data, which is a dictionary of ContentData objects with tkinter elements
            self.passages_data = {} # TODO: Redundant, remove need to remove passages at some point
            self.generate_passages_data()

    def generate_passages_data(self):
        passages_list = self.passages.get_keys()
        for i, name in enumerate(passages_list):
            p = self.passages[name]
            if name in self.script_parser.events:
                self.passages_data[name] = ContentData(p.pid, p.name, p.tags, p.content,
                                                       self.script_parser.events[name], p.position, p.size)
            else:
                self.passages_data[name] = ContentData(p.pid, p.name, p.tags, p.content, None, p.position,
                                                       p.size)
