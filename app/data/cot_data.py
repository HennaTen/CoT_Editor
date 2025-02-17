# Shouldn't be used in the code, but it's here for reference
from app.tools.color import rgb
from app.tools.json_convert import convert_to_json
from pathlib import Path

event_tags = [
    'prereq',  # the given event (identified by story passage) must have happened first
    'checkvar',  # the given value (in story variables) must be truthy
    'kink',  # when the given kink must be present in the player's $kinkcontent, otherwise the event is filtered out
    'chance', # 0.0 to 1.0 are the odds of this event being valid -- you are usually better off just using frequency or relying on the base event chance but this can be useful sometimes
    'genders',  # which will select the event only if the PC's gender is in the list
    'genderprefs',  # which must include one or more genders within the PC's sexual preferences
    'majors',  # for specific majors (college class events)
    'class types',  # for specific class types (valid values: classroom, lecture, lab)
    'courses',  # for specific valid courses (i.e. 'Intro to Psychology', 'Photography I' etc)
    'peoplehere',   # number of NPCs at this location for the event to fire (# of NPCs must be >= this # except that 0 means 0)
    'peopleherelt',  # number of NPCs at this location less than the given number
    'inclinations',  # if the PC has any of these inclinations
    'noinclinations',  # if the PC does not have any of these inclinations
    'npc inclinations',  # if someone with these inclinations needs to be present at the scene
    'desired relationships',   # what the npc wants with the pc (can be friend, date, rival, fuckbuddy, hatefuck, indifferent)
    'niche',  # which will only fire if the NPC in the specified narrative niche is present
    'noniche',  # will only fire if the NPC is not present
    'from day',  # which will discard the event unless $gameday is >= to
    'days since',  # which will discard the event if it previously occurred < this number of days ago
    'before day',  # event no longer valid after this day
    'unique',   # set to true if the event should fire only one time ever (these should be rare and usually set up future events)
    'horny',   # if it requires a pc horniness level (set to 0 for no horniness, 1 if requiring 1-2 horniness, 2 for 2 horniness) (if set to 1, happens at increased frequency when pc horniness is 2)
    'genders',  # for certain genders only... use sparingly
    'parts',  # for certain body parts only
    'hours',  # starting and ending hours for this event
    'timeofday',  # which can be (exact strings) morning/day/afternoon/night
    'weekdays',  # happens on these weekdays only (Monday, Saturday, etc)
    'skill',  # array of [skill, level] as a prereq
    'locations',  # event only happens at these locations
    'locationblocks',  # as above but for locationblocks
    'nolocations',  # event excluded if at these locations
    'nolocationblocks',  # as above but for locationblocks
    'toys',  # event excluded unless player has a toy of the given types
    'equippedtoys',  # event excluded unless player has a currently equipped/worn toy of the given types
    'reputation',  # an array of [reputation type, amount to exceed, (optional) population type]
    'findnpc', # will fire the event of an NPC matching the given person-picker conditions are met, and $eventnpc will be set to this person
    'crush', # if true, finds a crushable NPC under default conditions (generally perfectly fine) and sets it to $eventnpc, but you can override these conditions by also including findnpc
    'findrelationship',   # will find an NPC of the given relationship(s) -- notably, whether they are originally at that location or not (by default, it'll pick any student; override with findnpcamong)
    'addrelationship',   # to find an NPC where the given relationship(s) is to be added among $peopleatlocation (or event.findnpcamong)
    'removerelationship',  # as above except for removing
]

special_tags = [
    "cleavage",  # if the player is showing cleavage or will show it if they bend over
    "skirt flip",  # if the player is wearing a skirt that may flip up (random chance)
    "upshorts",  # if the player is wearing shorts that may give a glimpse up the leg (random chance)
    "downblouse",  # if the player is wearing a shirt that one may be able to see all the way down (random chance)
    "nipslip",  # if the player is wearing a top that may accidentally reveal their bra cup or nipple (random chance)
    "underboob", # if the player is wearing a crop top that may accidentally fully reveal the breast from underneath (random chance)
    "under access",  # if the player is wearing a skirt or dress, basically
    "underwear access",  # if underwear (or naked bits) is accessible under skirt/dress
    "elastic waistband",  # if pants have an elastic waistband (i.e. easily accessed or pulled down)
    "no underwear",  # if the player is not wearing underwear (specifically covering the crotch)
    "no bra",  # if the player has breasts and is not wearing a bra
    "bra visible",  # if the player has breasts and their bra is visible
    "underwear visible",  # if the player's underwear is visible
    "topless",  # if chest is uncovered (not necessarily for breasts only!)
    "bottomless",  # if the PC is bottomless
    "boobless topless",  # if chest is uncovered and player does not have breasts
    "shirt",  # if pc is wearing shirt/top
    "pants",  # if PC is wearing pants (dress counts, so consider also using the 'no dress' tag if that matters)
    "dress",  # if pc is wearing a dress (not just skirt)
    "no dress",  # if pc is NOT wearing a dress
    "drunk",  # if PC is drunk (drunkenness > 400)
    "passoutdrunk",  # if PC is passout drunk (drunkenness > 800)
    "sober",  # if PC is... not drunk!
    "hard nipples",  # if the PC has visibly hard nipples
    "muscles",  # if the PC is masc and has visible muscles (skintight or no shirt)
    "bulge",  # if the PC is wearing something tight enough to show bulge (not necessarily erect)
    "hardon",  # as above, but just for erections
    "anonymous",  # only if player is anonymous (wearing mask)
    "not anonymous",  # only if player is not anonymous
]

needs = [
    "Rest",
    "Relaxation",
    "Attention",
    "Food",
    "Bladder",
    "Hygiene",
    "Composure",
    "Release",
    "Arousal",
    "Satisfaction",
    "Pain",
    "Humiliation",
    "Drunkenness",
]

pronoun_female = {
    "psc": "She",
    "poc": "Her",
    "ppc": "Her",
    "prc": "Herself",
    "pqc": "Hers",
    "ps": "she",
    "po": "her",
    "pp": "her",
    "pr": "herself",
    "pq": "hers",
    "noun": "woman",
    "youngnoun": "girl",
    "casualnoun": "girl",
    "mrs": "Mrs.",
    "miss": "Miss",
    "ms": "Ms.",
    "partner": "girlfriend",
    "spouse": "wife",
    "master": "Mistress",
    "pss": "she's",
    "pssc": "She's",
    "pshas": "she's",
    "pshasc": "She's",
}

pronoun_male = {
    "psc": "He",
    "poc": "Him",
    "ppc": "His",
    "prc": "Himself",
    "pqc": "His",
    "ps": "he",
    "po": "him",
    "pp": "his",
    "pr": "himself",
    "pq": "his",
    "noun": "man",
    "youngnoun": "boy",
    "casualnoun": "guy",
    "mrs": "Mr.",
    "miss": "Mr.",
    "ms": "Mr.",
    "partner": "boyfriend",
    "spouse": "husband",
    "master": "Master",
    "pss": "he's",
    "pssc": "He's",
    "pshas": "he's",
    "pshasc": "He's",
}

pronoun_nonbinary = {
    "psc": "They",
    "poc": "Them",
    "ppc": "Their",
    "prc": "Themself",
    "pqc": "Theirs",
    "ps": "they",
    "po": "them",
    "pp": "their",
    "pr": "themself",
    "pq": "theirs",
    "noun": "person",
    "youngnoun": "kid",
    "casualnoun": "kid",
    "mrs": "Mx.",
    "miss": "Mx",
    "ms": "Mx.",
    "partner": "partner",
    "spouse": "spouse",
    "master": "Master",
    "pss": "they're",
    "pssc": "They're",
    "pshas": "they've",
    "pshasc": "They've",
}

pronoun_tags = {
    "<<psc>>": "He|She|They",
    "<<poc>>": "Him|Her|Them",
    "<<ppc>>": "His|Her|Their",
    "<<prc>>": "Himself|Herself|Themself",
    "<<pqc>>": "His|Hers|Theirs",
    "<<ps>>": "he|she|they",
    "<<po>>": "him|her|them",
    "<<pp>>": "his|her|their",
    "<<pr>>": "himself|herself|themself",
    "<<pq>>": "his|hers|theirs",
    "<<noun>>": "man|woman|person",
    "<<youngnoun>>": "boy|girl|kid",
    "<<casualnoun>>": "guy|girl|kid",
    "<<mrs>>": "Mr.|Mrs.|Mx.",
    "<<miss>>": "Mr.|Miss|Mx",
    "<<ms>>": "Mr.|Ms.|Mx.",
    "<<partner>>": "boyfriend|girlfriend|partner",
    "<<spouse>>": "husband|wife|spouse",
    "<<master>>": "Master|Mistress|Master",
    "<<pss>>": "he's|she's|they're",
    "<<pssc>>": "He's|She's|They're",
    "<<pshas>>": "he's|she's|they've",
    "<<pshasc>>": "He's|She's|They've",
}

color_classes = {
    "sexy": {
        "begin": "<<highlight sexy>>",
        "end": "<</highlight>>",
        "background":rgb(196, 76, 142)
    },
    "romantic": {
        "begin": "<<highlight romantic>>",
        "end": "<</highlight>>",
        "background": rgb(245, 65, 89)
    },
    "festive": {
        "begin": "<<highlight festive>>",
        "end": "<</highlight>>",
        "background": rgb(202, 58, 94)
    },
    "gold": {
        "begin": "<<highlight gold>>",
        "end": "<</highlight>>",
        "background": rgb(216, 219, 29)
    },
    "mainskill": {
        "begin": "<<highlight mainskill>>",
        "end": "<</highlight>>",
        "background": rgb(179, 40, 116)
    },
    "otherskill": {
        "begin": "<<highlight otherskill>>",
        "end": "<</highlight>>",
        "background": rgb(119, 191, 224)
    },
    "decreaseneed": {
        "begin": "<<highlight decreaseneed>>",
        "end": "<</highlight>>",
        "background": rgb(194, 51, 32)
    },
    "increaseneed": {
        "begin": "<<highlight increaseneed>>",
        "end": "<</highlight>>",
        "background": rgb(57, 160, 26)
    },
    "equalneed": {
        "begin": "<<highlight equalneed>>",
        "end": "<</highlight>>",
        "background": rgb(102, 108, 109)
    },
    "pee": {
        "begin": "<<highlight pee>>",
        "end": "<</highlight>>",
        "background": rgb(221, 209, 101)
    },
    "cash": {
        "begin": "<<highlight cash>>",
        "end": "<</highlight>>",
        "background": rgb(58, 148, 66)
    },
    "notice": {
        "begin": "<<highlight notice>>",
        "end": "<</highlight>>",
        "background": rgb(108, 208, 226)
    },
    "noticedark": {
        "begin": "<<highlight noticedark>>",
        "end": "<</highlight>>",
        "background": rgb(66, 131, 143)
    },
    "bad": {
        "begin": "<<highlight bad>>",
        "end": "<</highlight>>",
        "background": rgb(190, 10, 10)
    },
    "ungood": {
        "begin": "<<highlight ungood>>",
        "end": "<</highlight>>",
        "background": rgb(187, 190, 10)
    },
    "unbad": {
        "begin": "<<highlight unbad>>",
        "end": "<</highlight>>",
        "background": rgb(118, 226, 108)
    },
    "female": {
        "begin": "<<highlight female>>",
        "end": "<</highlight>>",
        "background": rgb(255, 0, 255)
    },
    "male": {
        "begin": "<<highlight male>>",
        "end": "<</highlight>>",
        "background": rgb(0, 0, 255)
    },
    "nonbinary": {
        "begin": "<<highlight nonbinary>>",
        "end": "<</highlight>>",
        "background": rgb(0, 255, 255)
    },
    "glow": {
        "begin": "<<highlight glow>>",
        "end": "<</highlight>>",
        "background": "#fff"
    },
}

"""
manwoman: noun
boygirl: youngnoun
guygirl: casualnoun
gendernoun: boygirl, unless age gte 25 manwoman
mrmrs: mrs
mrmiss: miss
mrms: ms
bfgf: partner
husbandwife: spouse
slutstud: if masc stud, else slut
sir: if masc sir, if femme ma'am, else boss
master: master
pcpetnamefrom: if masc handsome, if femme girl, else sexy, unless age gte 40 if masc handsome, else honey
"""

if __name__ == '__main__':
    convert_to_json(color_classes, Path("../../config/containers/highlight.json"))