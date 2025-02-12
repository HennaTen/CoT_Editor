import re
from app.data.cot_data import event_tags
from app.parser.elements.event import Event


class TWUserScriptParser:  # TODO: Work in progress
    def __init__(self, soup):
        self.script_content = self.get_twine_user_script(soup)
        self.events = self.get_events()

    def get_twine_user_script(self, soup):
        script = soup.find('script', {'id': 'twine-user-script'})
        return script.get_text()

    def get_events(self):
        events = {}
        # Find setup.Events.db =
        event_db = re.search(r'setup.Events.db =([\s\S]*?);', self.script_content).group(1)
        # print(f"event_db: {event_db}")
        # Find all events inside the brackets

        # TODO: fix issue when there are brackets inside the event. Ex: findnpc: {costume: true},
        #  https://regexr.com/
        #  Should be fixed, need to confirm

        # Use a delimiter with r"},[\s]*{"
        event_list = re.split(r"},[\s]*{", event_db)
        # print(len(event_list))
        # print(f"event_list: {event_list}, {len(event_list)}")
        for event in event_list:
            # print(f"event: {event}")
            # Find passage
            passage = re.search(r'passage: "(.*?)"', event).group(1)
            # Find tags
            tags = re.search(r'tags: \[(.*?)\]', event).group(1)
            tags = tags.replace('"', "").split(", ")
            # Find frequency
            frequency = re.search(r'frequency: (\d+)', event).group(1)

            # TODO: Find additional tags using additional_tags, saving them in a dictionary
            #  Fix the regex to fit the datas
            additional_tags = {}
            for tag in event_tags:
                match = re.search(f"{tag}: (.*?),", event)
                if match:
                    additional_tags[tag] = match.group(1)

            events[passage] = Event(passage, tags, frequency, additional_tags)

        # print(f"events[EncounterActs]: {events['EncounterActs']}")
        return events
