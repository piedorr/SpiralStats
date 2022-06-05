import csv
import json
from composition import Composition

uids = {}

# Load all the character names
with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

def main():
    for phase in ["2.2b"]:
        stats = open("../data/raw_csvs/" + phase + ".csv")
        reader = csv.reader(stats)
        col_names = next(reader)
        full_table = []
        for line in reader:
            full_table.append(line)

        all_comps = form_comps(col_names, full_table, phase)
        write_comps(all_comps)

def bool_chars(row, cols, start, end):
    comp = []
    for i in range(start, end):
        if row[i] == '1':
            comp.append(cols[i])
    return comp

def four_chars(row, cols):
    return [row[i] for i in cols]

def form_comps(col_names, table, patch):
    comps = []
    room = col_names.index('half')
    if patch == "1.5a" or patch == "1.5b":
        start = col_names.index("Albedo")
        end = start + col_names.index("Zhongli")
        for row in table:
            comps.append(Composition(row[0], bool_chars(row, col_names, start, end),
                                     patch, row[room]))
    else:
        indexes = [col_names.index("ch1"), col_names.index("ch2"),
                   col_names.index("ch3"), col_names.index("ch4")]
        for row in table:
            comp_chars = four_chars(row, indexes)
            for char in comp_chars:
                if char not in CHARACTERS.keys() and char != "":
                    print("bad char name: " + char)
            comps.append(Composition(row[0], comp_chars, patch, row[room]))
    return comps

def write_comps(comps):
    with open('../data/compositions.csv', 'a') as out_file:
        if out_file.tell() == 0:
            out_file.write("uid,phase,room," + ",".join(list(CHARACTERS.keys())) + "\n")
        for comp in comps:
            out_file.write(comp_string(comp))

def comp_string(comp):
    builder = comp.player + "," + comp.phase + "," + comp.room
    for char in CHARACTERS:
        if comp.char_presence[char]:
            builder += ",1"
        else:
            builder += ",0"
    return builder + "\n"

if __name__ == '__main__':
    main()
