from app.parser.elements.tw_passage_data import TWPassageData


class TWPassageDataManager:
    def __init__(self, soup):
        self.soup = soup
        self.passages = self.get_passages()

    def get_passages(self, ):
        passages = {}
        for passage in self.soup.find_all('tw-passagedata'):
            pid = passage['pid']
            name = passage['name']
            tags = passage['tags']
            position = passage['position']
            size = passage['size']
            content = passage.get_text()
            passages[name] = TWPassageData(pid, name, tags, position, size, content)
        return passages

    def get_keys(self):
        list_key = []
        for key in self.passages.keys():
            list_key.append(key)
        return list_key

    def __str__(self):
        return f"passages: {self.passages}"

    def __getitem__(self, item):
        return self.passages[item]