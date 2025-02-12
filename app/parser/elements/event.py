class Event:  # TODO: WIP
    """
    # Found in setup.Events.db[]
    // the event database!
    // this is centralized logic for picking from a set of random events that can happen
    // 'tags' are most important: the function searching for events will need all of its given tags to be present
    // however, the event can still be selected if it has tags that aren't being looked for (exceptions below)

    // example: if the tags you're searching for are "green", "apple"
    // then events tagged with just "apple" (lacking "green") will be discarded
    // however if you're only searching for tag "apple" then an event tagged "red", "apple" can be selected

    // event picking doesn't have to use this framework, but it'll generally save you some work if it does

    SEE data.cot_data.event_tags

    // take care with events that exclude entire genders and the like
    // if they're minor things anyway, then ok, or if you have an event for each gender, then great
    // but generally, try to include all types of characters, just vary the scene accordingly
    // also, do not expect gender and body parts to necessarily correlate, it's the 21st century
    // use $pc.has_parts("vagina") or whatever

    // we also have many special tags:
    SEE data.cot_data.special_tags
    // using any of these tags will cause the event to be discarded if the player doesn't fit the circumstances

    #     Ex:
    #     {
    #         passage: "EventDiningHallUneventful",
    #         tags: ["job", "dining hall"],
    #         frequency: 60,
    #     },
    """

    def __init__(self, passage, tags, frequency, additional_tags=None):
        self.passage = passage
        self.tags = tags
        self.frequency = frequency
        self.additional_tags = additional_tags

    def __str__(self):
        return (f"passage: {self.passage}, tags: {self.tags}, self.frequency: {self.frequency}, "
                f"other: {self.additional_tags}")
