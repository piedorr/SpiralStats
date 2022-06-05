import json
import operator

ROOMS = ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]
with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

def ownership(players, chambers=ROOMS):
    # Create the dict
    owns = {}
    for phase in players:
        owns[phase] = {}

    # Add a sub sub dict for each char
    for phase in owns:
        for character in CHARACTERS:
            owns[phase][character] = {
                "flat": 0,
                "percent": 0.00,
                "cons_freq": {}
            }
            for i in range (7):
                owns[phase][character]["cons_freq"][i] = {
                    "flat": 0,
                    "percent": 0,
                }

        # Tally the amount that each char is owned
        total = 0
        for player in players[phase]:
            total += 1
            for character in CHARACTERS:
                if players[phase][player].owned[character]:
                    char_name = character
                    owns[phase][char_name]["flat"] += 1
                    owns[phase][char_name]["cons_freq"][
                        players[phase][player].owned[character]["cons"]
                    ]["flat"] += 1
        total /= 100.0
        for char in owns[phase]:
            own_flat = owns[phase][char]["flat"] / 100.0
            if own_flat > 0:
                if char in {"Traveler-A", "Traveler-G", "Traveler-E"}:
                    # Cons usage is only added for floor 12
                    if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                        for cons in owns[phase][char]["cons_freq"]:
                            if owns[phase][char]["cons_freq"][cons]["flat"] > 15:
                                owns[phase][char]["cons_freq"][cons]["percent"] = int(round(
                                    owns[phase][char]["cons_freq"][cons]["flat"] / own_flat, 0
                                ))
                            else:
                                owns[phase][char]["cons_freq"][cons]["percent"] = "-"
                    owns[phase][char]["percent"] = 100.0
                    owns[phase][char]["flat"] = int(total * 100)

                else:
                    # Cons usage is only added for floor 12
                    if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                        for cons in owns[phase][char]["cons_freq"]:
                            if owns[phase][char]["cons_freq"][cons]["flat"] > 15:
                                owns[phase][char]["cons_freq"][cons]["percent"] = int(round(
                                    owns[phase][char]["cons_freq"][cons]["flat"] / total, 0
                                ))
                            else:
                                owns[phase][char]["cons_freq"][cons]["percent"] = "-"
                    owns[phase][char]["percent"] = round(
                        owns[phase][char]["flat"] / total, 2
                    )
    
    # print(json.dumps(owns,indent=4))

    return owns

def appearances(players, owns, chambers=ROOMS, offset=3, info_char=False):
    appears = {}
    num_players = {}
    for phase in players:
        appears[phase] = {}
        num_players[phase] = 0

        for character in CHARACTERS:
            appears[phase][character] = {
                "flat": 0,
                "percent": 0.00,
                "weap_freq": {},
                "arti_freq": {},
                "cons_freq": {}
            }
            for i in range (7):
                appears[phase][character]["cons_freq"][i] = {
                    "flat": 0,
                    "percent": 0,
                }

        # There's probably a better way to cache these things
        for player in players[phase].values():
            num_players[phase] += 1
            for char in CHARACTERS:
                for chamber in chambers:
                    if player.chambers[chamber] == None:
                        continue
                    if player.chambers[chamber].char_presence[char]:
                        char_name = char
                        appears[phase][char_name]["flat"] += 1
                        # In case of character in comp data missing in character data
                        # print(str(player.player))
                        # print(str(player.owned[char]["cons"]))
                        appears[phase][char_name]["cons_freq"][player.owned[char]["cons"]]["flat"] += 1

                        if player.owned[char]["weapon"] != "":
                            if player.owned[char]["weapon"] in appears[phase][char_name]["weap_freq"]:
                                appears[phase][char_name]["weap_freq"][player.owned[char]["weapon"]] += 1
                            else:
                                appears[phase][char_name]["weap_freq"][player.owned[char]["weapon"]] = 1

                        if player.owned[char]["artifacts"] != "":
                            if player.owned[char]["artifacts"] in appears[phase][char_name]["arti_freq"]:
                                appears[phase][char_name]["arti_freq"][player.owned[char]["artifacts"]] += 1
                            else:
                                appears[phase][char_name]["arti_freq"][player.owned[char]["artifacts"]] = 1

        total = num_players[phase] * offset / 100.0
        for char in appears[phase]:
            appears[phase][char]["percent"] = round(
                appears[phase][char]["flat"] / total, 2
            )

            if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                # Calculate constellations
                if owns[phase][char]["flat"] > 0:
                    for cons in appears[phase][char]["cons_freq"]:
                        if owns[phase][char]["cons_freq"][cons]["flat"] > 15:
                            appears[phase][char]["cons_freq"][cons]["percent"] = int(round(
                                appears[phase][char]["cons_freq"][cons]["flat"] / total, 0
                            ))
                        else:
                            appears[phase][char]["cons_freq"][cons]["percent"] = "-"

                # Calculate weapons
                app_flat = appears[phase][char]["flat"] / 100.0
                sorted_weapons = (sorted(
                    appears[phase][char]["weap_freq"].items(),
                    key = operator.itemgetter(1),
                    reverse=True
                ))
                appears[phase][char]["weap_freq"] = {k: v for k, v in sorted_weapons}
                for weapon in appears[phase][char]["weap_freq"]:
                    # If a gear appears >15 times, include it
                    # Because there might be 1* gears
                    # If it's for character infographic, include all gears
                    if appears[phase][char]["weap_freq"][weapon] > 15 or info_char:
                        appears[phase][char]["weap_freq"][weapon] = round(
                            appears[phase][char]["weap_freq"][weapon] / app_flat, 2
                        )
                    else:
                        appears[phase][char]["weap_freq"][weapon] = "-"

                # Calculate artifacts
                sorted_arti = (sorted(
                    appears[phase][char]["arti_freq"].items(),
                    key = operator.itemgetter(1),
                    reverse=True
                ))
                appears[phase][char]["arti_freq"] = {k: v for k, v in sorted_arti}
                for arti in appears[phase][char]["arti_freq"]:
                    # If a gear appears >15 times, include it
                    # Because there might be 1* gears
                    # If it's for character infographic, include all gears
                    if appears[phase][char]["arti_freq"][arti] > 15 or info_char:
                        appears[phase][char]["arti_freq"][arti] = round(
                            appears[phase][char]["arti_freq"][arti] / app_flat, 2
                        )
                    else:
                        appears[phase][char]["arti_freq"][arti] = "-"
    return appears

def usages(owns, appears, chambers=ROOMS, offset=3):
    uses = {}
    past_usage = {
        "Kaedehara Kazuha": 89.88, "Kamisato Ayaka": 85.57, "Venti": 85.11, "Sangonomiya Kokomi": 83.61, "Kamisato Ayato": 71.93, "Shenhe": 55.28, "Zhongli": 53.11, "Ganyu": 50.75, "Raiden Shogun": 50.34, "Tartaglia": 34.45, "Yae Miko": 24.92, "Hu Tao": 14.27, "Eula": 13.19, "Albedo": 11.33, "Xiao": 11.16, "Arataki Itto": 8.45, "Yoimiya": 4.37, "Klee": 1.70, "Mona": 52.96, "Jean": 13.56, "Keqing": 2.85, "Qiqi": 2.22, "Diluc": 1.00, "Xingqiu": 71.32, "Bennett": 56.07, "Diona": 48.03, "Sucrose": 37.31, "Rosaria": 25.17, "Xiangling": 23.56, "Fischl": 17.20, "Beidou": 11.40, "Barbara": 8.72, "Kaeya": 6.97, "Chongyun": 6.41, "Yun Jin": 3.86, "Kujou Sara": 2.10, "Noelle": 2.06, "Gorou": 1.99, "Sayu": 1.10, "Ningguang": 1.01, "Lisa": 0.77, "Thoma": 0.57, "Traveler-A": 0.56, "Amber": 0.33, "Traveler-G": 0.30, "Yanfei": 0.24, "Traveler-E": 0.23, "Xinyan": 0.16, "Razor": 0.14, "Aloy": 0.09
    }
    past_usage_11 = {
        "Kaedehara Kazuha": 90.30, "Venti": 90.26, "Kamisato Ayaka": 70.19, "Sangonomiya Kokomi": 68.07, "Kamisato Ayato": 59.59, "Zhongli": 51.65, "Raiden Shogun": 50.90, "Ganyu": 48.64, "Shenhe": 47.88, "Xiao": 31.17, "Yae Miko": 26.35, "Tartaglia": 26.32, "Albedo": 25.73, "Hu Tao": 20.19, "Eula": 15.60, "Arataki Itto": 14.95, "Yoimiya": 13.00, "Klee": 4.83, "Mona": 41.64, "Jean": 14.74, "Keqing": 3.07, "Diluc": 2.92, "Qiqi": 2.33, "Bennett": 70.01, "Xingqiu": 54.16, "Sucrose": 50.61, "Diona": 40.51, "Xiangling": 35.83, "Rosaria": 17.23, "Fischl": 15.66, "Beidou": 9.81, "Kujou Sara": 5.27, "Kaeya": 4.49, "Yun Jin": 4.26, "Barbara": 3.97, "Gorou": 3.95, "Chongyun": 2.90, "Noelle": 2.64, "Ningguang": 2.26, "Traveler-G": 1.40, "Thoma": 1.26, "Yanfei": 0.85, "Traveler-A": 0.79, "Sayu": 0.78, "Lisa": 0.63, "Xinyan": 0.42, "Amber": 0.37, "Traveler-E": 0.35, "Razor": 0.33, "Aloy": 0.24
    }
    for phase in owns:
        uses[phase] = {}
        rates = []
        for char in owns[phase]:
            if owns[phase][char]["flat"] > 0:
                rate = round(appears[phase][char]["flat"] / (owns[phase][char]["flat"] * offset / 100.0), 2)
                rates.append(rate)

                uses[phase][char] = {
                    "app": appears[phase][char]["percent"],
                    "app_flat": appears[phase][char]["flat"],
                    "own": owns[phase][char]["percent"],
                    "usage" : rate,
                    "diff": "-",
                    "diff_11": "-",
                    "rarity": CHARACTERS[char]["availability"],
                    "weapons" : {},
                    "artifacts" : {},
                    "cons_usage": {}
                }

                if char in past_usage:
                    uses[phase][char]["diff"] = round(rate - past_usage[char], 2)

                if char in past_usage_11:
                    uses[phase][char]["diff_11"] = round(rate - past_usage_11[char], 2)

                if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                    for i in range (7):
                        uses[phase][char]["cons_usage"][i] = {
                            "app": "-",
                            "own": "-",
                            "usage": "-",
                        }

                    weapons = list(appears[phase][char]["weap_freq"])
                    i = 0
                    while i < 6:
                        if i >= len(weapons):
                            uses[phase][char]["weapons"][i] = "-"
                        else:
                            uses[phase][char]["weapons"][weapons[i]] = appears[phase][char]["weap_freq"][weapons[i]]
                        i += 1

                    artifacts = list(appears[phase][char]["arti_freq"])
                    i = 0
                    while i < 6:
                        if i >= len(artifacts):
                            uses[phase][char]["artifacts"][i] = "-"
                        else:
                            uses[phase][char]["artifacts"][artifacts[i]] = appears[phase][char]["arti_freq"][artifacts[i]]
                        i += 1

                    for i in range (7):
                        if owns[phase][char]["cons_freq"][i]["flat"] > 15:
                            uses[phase][char]["cons_usage"][i]["app"] = appears[phase][char]["cons_freq"][i]["percent"]
                            uses[phase][char]["cons_usage"][i]["own"] = owns[phase][char]["cons_freq"][i]["percent"]
                            if char in {"Traveler-A", "Traveler-G", "Traveler-E"}:
                                uses[phase][char]["cons_usage"][i]["usage"] = round(
                                    appears[phase][char]["cons_freq"][i]["flat"]  / (owns[phase][char]["cons_freq"][i]["flat"] * (
                                            owns[phase][char]["flat"] / owns[phase][char]["cons_freq"][i]["flat"]
                                        ) * offset / 100.0), 2
                                )
                            else:
                                uses[phase][char]["cons_usage"][i]["usage"] = round(
                                    appears[phase][char]["cons_freq"][i]["flat"] / (owns[phase][char]["cons_freq"][i]["flat"] * offset / 100.0), 2
                                )
        rates.sort(reverse=True)
        for char in uses[phase]:
            uses[phase][char]["rank"] = rates.index(uses[phase][char]["usage"]) + 1
    return uses
