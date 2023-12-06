import sys
sys.path.append('../Comps/')

import os
import csv
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
# for row in build:
#     chars.append(row[0])
chars = ["Furina", "Baizhu", "Charlotte", "Beidou", "Collei", "Cyno", "Kamisato Ayato", "Kirara", "Xiangling", "Kuki Shinobu"]
stats = {}
median = {}
mean = {}
sample = {}
weapons = {}
copy_weapons = {}

spiral_rows = {}
for spiral_row in spiral:
    if spiral_row[1] == "12":
        if spiral_row[0] not in spiral_rows:
            spiral_rows[spiral_row[0]] = {}
        spiral_rows[spiral_row[0]][spiral_row[3]] = [spiral_row[4], spiral_row[5], spiral_row[6], spiral_row[7]]

for char in chars:
    stats[char] = {}
    median[char] = {}
    mean[char] = {}
    sample[char] = {}
    weapons[char] = []

    for row in build:
        if row[0] == char:
            for j in range (14,29,2):
                if row[j]!="-":
                    weapons[char].append(row[j])
                    stats[char][row[j]] = {
                        "name": row[j],
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
                        "cryo": []
                    }
                    median[char][row[j]] = {
                        "name": row[j],
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
                        "cryo": 0
                    }
                    mean[char][row[j]] = {
                        "name": row[j],
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
                        "cryo": 0
                    }
                    sample[char][row[j]] = 0
            break

statkeys = list(stats[chars[0]][weapons[chars[0]][0]].keys())

for row in data:
    if row[2] == "":
        continue
    # if (row[2].isnumeric()):
    #     row.insert(2,"Nilou")
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
    # if row[2] == char and float(row[13]) < 100: #EM < 100
        # for chars_row in chars:
        #     if chars_row[2] == "Traveler":
        #         if chars_row[3] == "Geo":
        #             chars_row[2] = "Traveler-G"
        #         elif chars_row[3] == "Anemo":
        #             chars_row[2] = "Traveler-A"
        #         elif chars_row[3] == "Electro":
        #             chars_row[2] = "Traveler-E"
        #         elif chars_row[3] == "Dendro":
        #             chars_row[2] = "Traveler-D"
        #     # if spiral_row[0] == chars_row[0] and chars_row[2] == char:
        #     if row[0] == chars_row[0] and chars_row[2] == char:
    if row[2] in chars:
        if row[0] in spiral_rows:
            for chamber_chars in spiral_rows[row[0]]:
                foundchar = resetfind()
                if row[2] in spiral_rows[row[0]][chamber_chars] or ("Traveler" in spiral_rows[row[0]][chamber_chars] and "Traveler" in row[2]):
                    foundchar["found"] = True
                for char in spiral_rows[row[0]][chamber_chars]:
                    findchars(char, foundchar)

                # if found and char_arti == "Gilded Dreams":
                # if found and ((float(row[9]) * 2) + float(row[10]) > 1.8 and float(row[18]) > 0.4):
                if foundchar["found"] and find_archetype(foundchar):
                    if row[24] in weapons[row[2]]:
                        sample[row[2]][row[24]] += 1
                        i = 3
                        for stat in stats[row[2]][row[24]]:
                            if stat != "name":
                                stats[row[2]][row[24]][stat].append(float(row[i]))
                                i += 1

for char in chars:
    copy_weapons[char] = weapons[char].copy()
    for weapon in copy_weapons[char]:
        if sample[char][weapon] > 0:
            # print()
            # print(weapon + ": " + str(sample[char][weapon]))
            for stat in stats[char][weapon]:
                skewness = 0
                if stat != "name":
                    if stat in ["attack_lvl", "skill_lvl", "burst_lvl", "max_hp", "atk", "dfns", "em"]:
                        median[char][weapon][stat] = round(statistics.median(stats[char][weapon][stat]), 2)
                        mean[char][weapon][stat] = round(statistics.mean(stats[char][weapon][stat]), 2)
                    else:
                        median[char][weapon][stat] = round(statistics.median(stats[char][weapon][stat]), 4)
                        mean[char][weapon][stat] = round(statistics.mean(stats[char][weapon][stat]), 4)
                    if mean[char][weapon][stat] > 0 and median[char][weapon][stat] > 0 and sample[char][weapon] > 5:
                        if stat not in ["attack_lvl", "skill_lvl", "burst_lvl","heal", "phys","pyro","electro","hydro","dendro","anemo","geo","cryo"]:
                            skewness = round(skew(stats[char][weapon][stat], axis=0, bias=True), 2)
                    if skewness < -1 or skewness > 1:
                        stats[char][weapon][stat] = str(median[char][weapon][stat])
                        # print(stat + ": " + str(mean[char][weapon][stat]) + ", " + str(median[char][weapon][stat]))
                        # # try:
                        # plt.hist(stats[char][weapon][stat])
                        # plt.show()
                        # # except Exception:
                        # #     pass
                        # # print("1 - Mean, 2 - Median: ")
                        # with keyboard.Events() as events:
                        #     event = events.get(1e6)
                        #     if event.key == keyboard.KeyCode.from_char('1'):
                        #         stats[char][weapon][stat] = str(mean[char][weapon][stat])
                        #     else:
                        #         stats[char][weapon][stat] = str(median[char][weapon][stat])
                    else:
                        stats[char][weapon][stat] = str(mean[char][weapon][stat])
        else:
            del stats[char][weapon]
            weapons[char].remove(weapon)

    csv_writer = csv.writer(open("results/" + char + "_weapons.csv", 'w', newline=''))
    if weapons[char] and stats[char]:
        csv_writer.writerow(stats[char][weapons[char][0]].keys())
        for weapon in weapons[char]:
            print(weapon + ": " + str(sample[char][weapon]))
            csv_writer.writerow(stats[char][weapon].values())
