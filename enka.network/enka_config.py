import csv
import json

# UIDS TO FETCH
current_phase = "Jul1"
phase_num = "3.7c"
with open("../char_results/" + current_phase + "/uids.csv", 'r', encoding='UTF8') as f:
    reader = csv.reader(f, delimiter=',')
    uids = list(reader)
uids = [int(uid[0]) for uid in uids]
uids = list(dict.fromkeys(uids))
# uids = uids[uids.index({uid})+1:]

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

traveler_ids = []
for char in characters.values():
    if "Traveler" in char["name"]:
        traveler_ids.append(int(char["id"].split("-")[0]))
