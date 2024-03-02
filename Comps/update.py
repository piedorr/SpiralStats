import json
import requests
import csv

response = requests.get("https://api.ambr.top/v2/en/reliquary")
artifacts = response.json()["data"]["items"]

with open('../data/artifacts.json') as artifact_file:
    artifacts2 = json.load(artifact_file)

artifacts_affixes = {}
for artifact in artifacts:
    if 4 in artifacts[artifact]["levelList"]:
        affix = list(artifacts[artifact]["affixList"].values())[0]

        if affix[-1] == ".":
            affix = affix[:-1]
        for i in ["is ", "DMG ", " Bonus", "Strength "]:
            affix = affix.replace(i, "")

        affix = affix.replace("increased by ", "+")
        if "Increases " in affix:
            affix = affix.replace("Increases ", "")
            affix = affix.replace("by ", "+")
        if "Gain a " in affix:
            affix = affix.replace("Gain a ", "")
            split = affix.split(" ")
            affix = split[1] + " +" + split[0]
        if "Healing" in affix:
            split = affix.split("+")
            affix = "Heal +" + split[1]

        affix = affix.replace("Energy Recharge", "ER")
        affix = affix.replace("CRIT Rate", "CR")
        affix = affix.replace("Normal and Charged Attack", "NA, CA")
        affix = affix.replace("Physical", "Phys")
        affix = affix.replace("Elemental Mastery", "EM")
        affix = affix.replace("Elemental ", "")

        if affix not in artifacts_affixes:
            artifacts_affixes[affix] = []
        artifacts_affixes[affix].append(artifacts[artifact]["name"])

for artifact in list(artifacts_affixes.keys()):
    if len(artifacts_affixes[artifact]) > 1 and artifact not in artifacts2:
        if len(artifact) > 12:
            print("Set name too long: " + artifact)
        else:
            add_arti = input("Add " + artifact + "? (y/n): ")
            if add_arti == "y":
                artifacts2[artifact] = artifacts_affixes[artifact]
    else:
        del artifacts_affixes[artifact]
print()

with open("../data/artifact_sets.json", "w") as out_file:
    out_file.write(json.dumps(artifacts,indent=4))

with open("../data/artifacts.json", "w") as out_file:
    out_file.write(json.dumps(artifacts2,indent=4))

weapon_types = {
    "WEAPON_SWORD_ONE_HAND": "Sword",
    "WEAPON_BOW": "Bow",
    "WEAPON_CATALYST": "Catalyst",
    "WEAPON_CLAYMORE": "Claymore",
    "WEAPON_POLE": "Polearm"
}
elements = {
    "Ice": "Cryo",
    "Wind": "Anemo",
    "Electric": "Electro",
    "Water": "Hydro",
    "Fire": "Pyro",
    "Grass": "Dendro",
    "Rock": "Geo"
}

with open('../data/characters.json') as char_file:
    chars1 = json.load(char_file)
response = requests.get("https://api.ambr.top/v2/en/avatar")
chars2 = response.json()["data"]["items"]

for char in chars2:
    char_name = chars2[char]["name"]
    if char_name == "Traveler":
        char_name = "Traveler-" + elements[chars2[char]["element"]].capitalize()[0]
    if char_name not in chars1:
        add_char = input("Add " + char_name + "? (y/n): ")
        if add_char == "y":
            chars1[char_name] = {
                "id": chars2[char]["id"],
                "name": char_name,
                "weapon": weapon_types[chars2[char]["weaponType"]],
                "element": elements[chars2[char]["element"]],
                "rarity": chars2[char]["rank"],
                "icon": chars2[char]["icon"],
                "route": chars2[char]["route"],
                "alt_name": None,
                "out_name": False,
                "availability": "4*"
            }
            if chars2[char]["rank"] == 5:
                if "Traveler" in char_name:
                    chars1[char_name]["rarity"] = 4
                    chars1[char_name]["availability"] = "Free"
                else:
                    # lim_char = input("Limited Character? (y/n): ")
                    # if lim_char == "y":
                    chars1[char_name]["availability"] = "Limited 5*"
                    # else:
                    #     chars1[char_name]["availability"] = "5*"
            on_field = input("On-field damage dealer? (y/n): ")
            if on_field == "y":
                chars1[char_name]["on_field"] = True
            else:
                chars1[char_name]["on_field"] = False
            role = input("DPS/Sub/Support? (0/1/2): ")
            if role == "0":
                chars1[char_name]["role"] = "DPS"
            elif role == "1":
                chars1[char_name]["role"] = "Sub-DPS"
            else:
                chars1[char_name]["role"] = "Support"

with open("../data/characters.json", "w") as out_file:
    out_file.write(json.dumps(chars1,indent=4))