import json
import os
from pathlib import Path
from app.data.cot_data import pronoun_tags


# Convert dictionary to JSON object
def convert_to_json(data, dest=Path("config/sample.json")):
    print(dest)
    # if destination folder does not exist, create it
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w") as outfile:
        json.dump(data, outfile, indent=4)

# Convert JSON object to dictionary
def convert_to_dict(src=Path("config/sample.json")):
    with open(src, "r") as infile:
        data = json.load(infile)
    return data

# convert every file in a directory to dictionary
def convert_dir_to_dict(src="config"):
    src = Path(src)
    data = {}
    for file in os.listdir(src):
        if file.endswith(".json"):
            name = file.split(".")[0]
            data[name] = convert_to_dict(Path(src) / file)
    return data

def main():
    convert_to_json(pronoun_tags, Path("config/translators/pronoun_tags.json"))

if __name__ == "__main__":
    main()