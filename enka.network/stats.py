import sys
sys.path.append('../Comps/')

import os
import operator
import statistics
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.stats import skew
from pynput import keyboard
from archetypes import *
from enka_config import phase_num

with open("output1.csv", 'r', encoding='UTF8') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)

    # include all
    data = list(reader)

    # # remove duplicates
    # data = []
    # uid_freq = {}
    # last_uid = "0"

    # # Append lines
    # for line in reader:
    #     if line[0] != last_uid:
    #         skip_uid = False
    #         # if line[0] in uid_freq or int(line[2].split("-")[0]) > 1:
    #         if line[0] in uid_freq:
    #             skip_uid = True
    #             # print("duplicate UID in comp: " + line[0])
    #         else:
    #             uid_freq[line[0]] = 1
    #     # else:
    #     #     uid_freq[line[0]] += 1
    #     last_uid = line[0]
    #     if not skip_uid:
    #         data.append(line)

if os.path.exists("../data/raw_csvs_real/"):
    f = open("../data/raw_csvs_real/" + phase_num + ".csv", 'r', encoding='UTF8')
else:
    f = open("../data/raw_csvs/" + phase_num + ".csv", 'r', encoding='UTF8')
reader = csv.reader(f, delimiter=',')
headers = next(reader)
spiral = list(reader)

with open("../char_results/12 build.csv", 'r', encoding='UTF8') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)
    build = list(reader)

chars = []
stats = {}
median = {}
mean = {}
mainstats = {}
substats = {}

spiral_rows = {}
for spiral_row in spiral:
    if spiral_row[1] == "12":
        if spiral_row[0] not in spiral_rows:
            spiral_rows[spiral_row[0]] = {}
        spiral_rows[spiral_row[0]][spiral_row[3]] = [spiral_row[4], spiral_row[5], spiral_row[6], spiral_row[7]]

for row in build:
    chars.append(row[0])
for char in chars:
    stats[char] = {
        "name": char,
        "attack_lvl": [],
        "skill_lvl": [],
        "burst_lvl": [],
        "max_hp": [],
        "atk": [],
        "dfns": [],
        "crate": [],
        "cdmg": [],
        "charge": [],
        "heal": [],
        "em": [],
        "phys": [],
        "pyro": [],
        "electro": [],
        "hydro": [],
        "dendro": [],
        "anemo": [],
        "geo": [],
        "cryo": [],
        "hp_sub": [],
        "atk_sub": [],
        "def_sub": [],
        "crate_sub": [],
        "cdmg_sub": [],
        "charge_sub": [],
        "em_sub": [],
        "sample_size": {}
    }
    mean[char] = {
        "attack_lvl": 0,
        "skill_lvl": 0,
        "burst_lvl": 0,
        "max_hp": 0,
        "atk": 0,
        "dfns": 0,
        "crate": 0,
        "cdmg": 0,
        "charge": 0,
        "heal": 0,
        "em": 0,
        "phys": 0,
        "pyro": 0,
        "electro": 0,
        "hydro": 0,
        "dendro": 0,
        "anemo": 0,
        "geo": 0,
        "cryo": 0,
        "hp_sub": 0,
        "atk_sub": 0,
        "def_sub": 0,
        "crate_sub": 0,
        "cdmg_sub": 0,
        "charge_sub": 0,
        "em_sub": 0
    }
    median[char] = {
        "attack_lvl": 0,
        "skill_lvl": 0,
        "burst_lvl": 0,
        "max_hp": 0,
        "atk": 0,
        "dfns": 0,
        "crate": 0,
        "cdmg": 0,
        "charge": 0,
        "heal": 0,
        "em": 0,
        "phys": 0,
        "pyro": 0,
        "electro": 0,
        "hydro": 0,
        "dendro": 0,
        "anemo": 0,
        "geo": 0,
        "cryo": 0,
        "hp_sub": 0,
        "atk_sub": 0,
        "def_sub": 0,
        "crate_sub": 0,
        "cdmg_sub": 0,
        "charge_sub": 0,
        "em_sub": 0
    }
    mainstats[char] = {
        "sands_stats": {},
        "goblet_stats": {},
        "helm_stats": {}
    }
ar = 0
ar_compile = {
    "56": 0,
    "57": 0,
    "58": 0,
    "59": 0,
    "60": 0
}
count = 0
uids = []
statkeys = list(stats[chars[0]].keys())
mainstatkeys = list(mainstats[chars[0]].keys())

for row in data:
    if not(row):
        continue
    # if (row[2].isnumeric()):
    #     row.insert(2,"Nilou")
    if row[0] not in uids and row[0] in spiral_rows:
        uids.append(row[0])
        ar+=int(row[22])
        count+=1
        if str(row[22]) in ar_compile:
            ar_compile[str(row[22])] += 1
        else:
            ar_compile["56"] += 1
    if row[2] == "":
        continue
    if row[2] == "Traveler":
        match row[23]:
            case "Rock":
                row[2] = "Traveler-G"
            case "Wind":
                row[2] = "Traveler-A"
            case "Electric":
                row[2] = "Traveler-E"
            case "Grass":
                row[2] = "Traveler-D"
            case "Water":
                row[2] = "Traveler-H"
            case "Fire":
                row[2] = "Traveler-P"
            case "Ice":
                row[2] = "Traveler-C"
    # for char in chars:
    #     if row[2] == char:
                # elif row[23] == "None":
                #     row[2] = "Traveler-D"

                # foundchar["found"] = False
                # for char_row in chardata:
                #     if char_row[0] == row[0] and not foundchar["found"]:
                #         if char_row[2] == char and char_row[3] == "Dendro":
                #             foundchar["found"] = True
    if row[0] in spiral_rows:
        for chamber_chars in spiral_rows[row[0]]:
            foundchar = resetfind()
            if row[2] in spiral_rows[row[0]][chamber_chars] or ("Traveler" in spiral_rows[row[0]][chamber_chars] and "Traveler" in row[2]):
                foundchar["found"] = True
            for char in spiral_rows[row[0]][chamber_chars]:
                findchars(char, foundchar)

            # if foundchar["found"] and char_arti == "Gilded Dreams":
            # if foundchar["found"] and ((float(row[9]) * 2) + float(row[10]) > 1.8 and float(row[18]) > 0.4):
            if foundchar["found"] and find_archetype(foundchar):
                stats[row[2]]["sample_size"][row[0]] = 1
                stats[row[2]]["em_sub"].append(float(row[32]))
                for i in range(1,20):
                    stats[row[2]][statkeys[i]].append(float(row[i+2]))
                for i in range(20,26):
                    stats[row[2]][statkeys[i]].append(float(row[i+6])/100)
                for i in range(3):
                    if row[i+33] in mainstats[row[2]][mainstatkeys[i]]:
                        mainstats[row[2]][mainstatkeys[i]][row[i+33]] += 1
                    else:
                        mainstats[row[2]][mainstatkeys[i]][row[i+33]] = 1
copy_chars = chars.copy()
for char in copy_chars:
    # print(artifacts[char])
    stats[char]["sample_size"] = len(stats[char]["sample_size"].keys())
    if stats[char]["sample_size"] > 0:
        # print(char + ": " + str(stats[char]["sample_size"]))
        # print()
        for stat in stats[char]:
            skewness = 0
            if not stats[char][stat]:
                stats[char][stat] = 0
            elif stat != "name" and stat != "sample_size":
                if stat in ["attack_lvl", "skill_lvl", "burst_lvl", "max_hp", "atk", "dfns", "em"]:
                    median[char][stat] = round(statistics.median(stats[char][stat]), 2)
                    mean[char][stat] = round(statistics.mean(stats[char][stat]), 2)
                else:
                    median[char][stat] = round(statistics.median(stats[char][stat]), 4)
                    mean[char][stat] = round(statistics.mean(stats[char][stat]), 4)
                if mean[char][stat] > 0 and median[char][stat] > 0 and stats[char]["sample_size"] > 5:
                    if stat not in ["attack_lvl", "skill_lvl", "burst_lvl","heal", "phys","pyro","electro","hydro","dendro","anemo","geo","cryo"]:
                        skewness = round(skew(stats[char][stat], axis=0, bias=True), 2)
                if skewness > 1:
                    stats[char][stat] = str(median[char][stat])
                    # print(stat + ": " + str(mean[char][stat]) + ", " + str(median[char][stat]))
                    # try:
                    #     plt.hist(stats[char][stat])
                    #     plt.show()
                    # except Exception:
                    #     pass
                    # # print("1 - Mean, 2 - Median: ")
                    # with keyboard.Events() as events:
                    #     event = events.get(1e6)
                    #     if event.key == keyboard.KeyCode.from_char('1'):
                    #         stats[char][stat] = str(mean[char][stat])
                    #     else:
                    #         stats[char][stat] = str(median[char][stat])
                else:
                    stats[char][stat] = str(mean[char][stat])

        for stat in mainstats[char]:
            sorted_stats = (sorted(
                mainstats[char][stat].items(),
                key = operator.itemgetter(1),
                reverse=True
            ))
            mainstats[char][stat] = {k: v for k, v in sorted_stats}
            for mainstat in mainstats[char][stat]:
                mainstats[char][stat][mainstat] = round(
                    mainstats[char][stat][mainstat] / stats[char]["sample_size"], 4
                )
            mainstatlist = list(mainstats[char][stat])
            i = 0
            while i < 3:
                if i >= len(mainstatlist):
                    stats[char][stat + "_" + str(i+1)] = "-"
                    stats[char][stat + "_" + str(i+1) + "_app"] = "-"
                else:
                    stats[char][stat + "_" + str(i+1)] = mainstatlist[i]
                    stats[char][stat + "_" + str(i+1) + "_app"] = mainstats[char][stat][mainstatlist[i]]
                i += 1

    else:
        del stats[char]
        chars.remove(char)

csv_writer = csv.writer(open("results/chars.csv", 'w', newline=''))
csv_writer.writerow(stats[chars[0]].keys())
csv_writer2 = csv.writer(open("results/demographic.csv", 'w', newline=''))
for char in chars:
    csv_writer.writerow(stats[char].values())
    csv_writer2.writerow([char + ": " + str(stats[char]["sample_size"])])

csv_writer = csv.writer(open("results/ar_compile.csv", 'w', newline=''))
csv_writer.writerow(ar_compile.keys())
csv_writer.writerow(ar_compile.values())

print("Average AR: ", (ar/count))
