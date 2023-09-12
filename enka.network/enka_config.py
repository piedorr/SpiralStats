import csv
import json
import os.path
import sys
sys.path.append('../Comps/')

from comp_rates_config import RECENT_PHASE
phase_num = RECENT_PHASE

# UIDS TO FETCH

# current_phase = "Jul2"
# if os.path.exists("../char_results/" + current_phase):
#     f = open("../char_results/" + current_phase + "/uids.csv", 'r', encoding='UTF8')
if os.path.exists("../char_results"):
    f = open("../char_results/uids.csv", 'r', encoding='UTF8')
    reader = csv.reader(f, delimiter=',')
    uids = list(reader)
    uids = [int(uid[0]) for uid in uids]
    uids = list(dict.fromkeys(uids))
    # uids = uids[uids.index({uid})+1:]
else:
    uids = []

filenum = 1
while os.path.exists("output" + str(filenum) + ".csv"):
    filenum += 1
filename = "output" + str(filenum)

# with open("output.csv", 'r', encoding='UTF8') as f:
#     reader = csv.reader(f, delimiter=',')
#     headers = next(reader)
#     output = list(reader)
# output = [int(uid[0]) for uid in output]
# output = list(dict.fromkeys(output))
# for uid in uids:
#     if uid in output:
#         uids.remove(uid)

# CHARACTER ID MATCHINGS
f = open('../data/characters.json')
characters = json.load(f)
char_ids = {}
for char in characters:
    char_ids[str(characters[char]["id"])] = characters[char].copy()
characters = char_ids

traveler_ids = [10000007]
for char in characters.values():
    if "Traveler" in char["name"]:
        traveler_ids.append(int(char["id"].split("-")[0]))
