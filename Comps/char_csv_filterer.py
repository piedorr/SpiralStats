import csv
import os
from comp_rates_config import RECENT_PHASE

def main():
    for phase in [RECENT_PHASE]:
        if os.path.exists("../data/raw_csvs_real/"):
            stats = open("../data/raw_csvs_real/" + phase + "_char.csv")
        else:
            stats = open("../data/raw_csvs/" + phase + "_char.csv")
        reader = csv.reader(stats)
        col_names = next(reader)
        indexes = find_vals(col_names)
        all_chars = []
        for line in reader:
            all_chars.append(build_char(indexes, line))

        write_chars(all_chars, phase)

def find_vals(col_names):
    """0: ID, 1: Character name. 2: Character level. 3: Character constellation.
       4: Character weapon. 5: Character artifact sets."""
    return [col_names.index("uid"), col_names.index("name"),
               col_names.index("level"), col_names.index("cons"),
               col_names.index("weapon"), col_names.index("artifacts"),
               col_names.index("element")]

def build_char(indexes, line):
    return {
        "uid": line[indexes[0]],
        "name": line[indexes[1]],
        "level": line[indexes[2]],
        "cons": line[indexes[3]],
        "weapon": line[indexes[4]],
        "artifacts": line[indexes[5]],
        "element": line[indexes[6]]
    }

def write_chars(all_chars, phase):
    with open('../data/phase_characters.csv', 'w') as out_file:
        if out_file.tell() == 0:
            out_file.write("uid,phase,name,level,cons,weapon,artifact,element\n")
        for char_data in all_chars:
            out_file.write(char_string(char_data, phase))
    
def char_string(char_data, phase):
    builder = char_data["uid"] + "," + phase + "," + char_data["name"] + "," + \
              char_data["level"] + "," + char_data["cons"] + "," + char_data["weapon"] + ","
    
    if "," in char_data["artifacts"]:
        builder += "\"" + char_data["artifacts"] + "\"," + char_data["element"] + "\n"
    else:
        builder += char_data["artifacts"] + "," + char_data["element"] + "\n"
    return builder

if __name__ == '__main__':
    main()
