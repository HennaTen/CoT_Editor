from bs4 import BeautifulSoup
from app.parser.tw_passage_data_manager import TWPassageDataManager
from app.parser.tw_user_script_parser import TWUserScriptParser


class CoTParser:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as file:
            # Read the file content
            html_content = file.read()

            # Parse the HTML content using BeautifulSoup
            self.soup = BeautifulSoup(html_content, 'html.parser')

            # Get all passages into custom class
            self.passages = TWPassageDataManager(self.soup)

            # Parse the Twine user script
            self.script_parser = TWUserScriptParser(self.soup)
