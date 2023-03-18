import json
import pandas as pd
import operator

ROOMS = ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]
global gear_app_threshold
gear_app_threshold = 0
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
                if char in {"Traveler-A", "Traveler-G", "Traveler-E", "Traveler-D"}:
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
    players_chars = {}
    for phase in players:
        appears[phase] = {}
        num_players[phase] = 0
        players_chars[phase] = {}
        comp_error = False
        error_comps = []

        for character in CHARACTERS:
            players_chars[phase][character] = []
            appears[phase][character] = {
                "flat": 0,
                "percent": 0.00,
                "weap_freq": {},
                "arti_freq": {},
                "cons_freq": {},
                "cons_avg": 0.00,
                "sample": 0
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
                    # foundPyro = False
                    # foundHydro = False
                    # foundNilou = False
                    # pyroChars = ["Bennett","Xiangling","Hu Tao","Thoma","Yoimiya","Yanfei","Xinyan","Diluc","Amber","Klee"]
                    # hydroChars = ["Mona","Sangonomiya Kokomi","Barbara","Xingqiu","Nilou","Candace","Yelan","Kamisato Ayato","Tartaglia"]
                    # testChar = 0
                    # while not foundPyro and testChar < len(pyroChars):
                    #     if player.chambers[chamber].char_presence[pyroChars[testChar]]:
                    #         foundPyro = True
                    #     testChar += 1
                    # testChar = 0
                    # while not foundHydro and testChar < len(hydroChars):
                    #     if player.chambers[chamber].char_presence[hydroChars[testChar]]:
                    #         foundHydro = True
                    #     testChar += 1
                    # if player.chambers[chamber].char_presence["Nilou"]:
                    #     foundNilou = True
                    # if player.chambers[chamber].char_presence[char] and not foundPyro and foundHydro:
                    # if player.chambers[chamber].char_presence[char] and foundNilou:
                    if player.chambers[chamber].char_presence[char]:
                        # to print the amount of players using a character, for char infographics
                        if player.player not in players_chars[phase][char]:
                            players_chars[phase][char].append(player.player)

                        char_name = char
                        appears[phase][char_name]["flat"] += 1
                        # In case of character in comp data missing from character data
                        if not player.owned[char]:
                            print("Comp data missing from character data: " + str(player.player) + ", " + str(char))
                            if player.player not in error_comps:
                                error_comps.append(player.player)
                            comp_error = True
                            continue
                        appears[phase][char_name]["cons_freq"][player.owned[char]["cons"]]["flat"] += 1
                        appears[phase][char_name]["cons_avg"] += player.owned[char]["cons"]

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

        if comp_error:
            df_char = pd.read_csv('../data/phase_characters.csv')
            df_spiral = pd.read_csv('../data/compositions.csv')
            df_char = df_char[~df_char['uid'].isin(error_comps)]
            df_spiral = df_spiral[~df_spiral['uid'].isin(error_comps)]
            df_char.to_csv("phase_characters.csv", index=False)
            df_spiral.to_csv("compositions.csv", index=False)
            raise ValueError("There are missing comps from character data.")

        total = num_players[phase] * offset / 100.0
        for char in appears[phase]:
            # # to print the amount of players using a character
            # print(str(char) + ": " + str(len(players_chars[phase][char])))
            appears[phase][char]["percent"] = round(
                appears[phase][char]["flat"] / total, 2
            )

            if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                appears[phase][char]["sample"] = len(players_chars[phase][char])
                # Calculate constellations
                if owns[phase][char]["flat"] > 0:
                    if appears[phase][char]["flat"] > 0:
                        appears[phase][char]["cons_avg"] /= appears[phase][char]["flat"]
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
                    if appears[phase][char]["weap_freq"][weapon] > gear_app_threshold or info_char:
                        appears[phase][char]["weap_freq"][weapon] = round(
                            appears[phase][char]["weap_freq"][weapon] / app_flat, 2
                        )
                    else:
                        appears[phase][char]["weap_freq"][weapon] = "-"

                # Remove flex artifacts
                appears[phase][char]["arti_freq"]["Flex"] = 0
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
                    if (appears[phase][char]["arti_freq"][arti] > gear_app_threshold or info_char) and arti != "Flex":
                        appears[phase][char]["arti_freq"][arti] = round(
                            appears[phase][char]["arti_freq"][arti] / app_flat, 2
                        )
                    else:
                        appears[phase][char]["arti_freq"][arti] = "-"
    return appears

def usages(owns, appears, chambers=ROOMS, offset=3):
    uses = {}
    past_usage = {
        "Nahida": 85.47, "Kaedehara Kazuha": 72.46, "Yelan": 69.52, "Bennett": 65.99, "Xingqiu": 64.77, "Zhongli": 64.49, "Raiden Shogun": 64.24, "Alhaitham": 55.44, "Sangonomiya Kokomi": 53.08, "Xiangling": 39.89, "Kuki Shinobu": 34.45, "Hu Tao": 33.79, "Yae Miko": 32.33, "Dehya": 30.73, "Nilou": 29.24, "Kamisato Ayato": 27.29, "Fischl": 21.37, "Tartaglia": 21.20, "Kamisato Ayaka": 19.00, "Yaoyao": 15.50, "Shenhe": 15.06, "Ganyu": 13.46, "Cyno": 13.43, "Albedo": 12.85, "Traveler-D": 11.93, "Xiao": 10.94, "Tighnari": 10.77, "Diona": 9.50, "Arataki Itto": 9.31, "Wanderer": 8.51, "Yoimiya": 8.46, "Eula": 7.87, "Mona": 7.72, "Jean": 7.33, "Keqing": 7.31, "Kujou Sara": 7.27, "Sucrose": 7.24, "Faruzan": 6.94, "Venti": 5.74, "Beidou": 4.39, "Gorou": 3.84, "Thoma": 3.35, "Klee": 2.96, "Collei": 2.63, "Yun Jin": 2.19, "Noelle": 1.92, "Diluc": 1.31, "Kaeya": 1.13, "Rosaria": 3.80, "Layla": 2.69, "Barbara": 2.52, "Lisa": 1.02, "Yanfei": 1.00, "Qiqi": 0.73, "Chongyun": 0.70, "Razor": 0.57, "Shikanoin Heizou": 0.53, "Ningguang": 0.34, "Sayu": 0.34, "Xinyan": 0.20, "Amber": 0.17, "Dori": 0.64, "Candace": 0.30, "Traveler-A": 0.17, "Aloy": 0.10, "Traveler-G": 0.08, "Traveler-E": 0.08
    }
    past_usage_11 = {
        "Nahida": 74.26, "Kaedehara Kazuha": 72.42, "Yelan": 61.27, "Sangonomiya Kokomi": 57.79, "Bennett": 54.67, "Zhongli": 54.24, "Xingqiu": 50.69, "Alhaitham": 50.62, "Kamisato Ayaka": 47.81, "Raiden Shogun": 42.52, "Shenhe": 41.48, "Venti": 38.58, "Dehya": 38.55, "Ganyu": 36.40, "Nilou": 31.85, "Xiangling": 30.59, "Yae Miko": 29.02, "Hu Tao": 27.62, "Kuki Shinobu": 27.11, "Kamisato Ayato": 26.47, "Fischl": 19.13, "Tartaglia": 17.61, "Yoimiya": 17.36, "Diona": 15.83, "Yaoyao": 15.16, "Wanderer": 15.08, "Mona": 15.06, "Tighnari": 12.19, "Albedo": 11.81, "Xiao": 11.38, "Rosaria": 11.17, "Traveler-D": 11.00, "Sucrose": 10.46, "Faruzan": 8.84, "Cyno": 7.88, "Eula": 6.93, "Arataki Itto": 5.98, "Layla": 5.71, "Keqing": 5.64, "Jean": 5.06, "Yun Jin": 4.33, "Kujou Sara": 4.14, "Barbara": 4.10, "Beidou": 3.94, "Kaeya": 3.87, "Klee": 3.29, "Thoma": 3.15, "Gorou": 2.79, "Chongyun": 2.26, "Collei": 2.21, "Noelle": 1.89, "Diluc": 1.73, "Qiqi": 1.43, "Shikanoin Heizou": 1.21, "Ningguang": 1.05, "Yanfei": 1.03, "Lisa": 0.82, "Razor": 0.51, "Candace": 0.47, "Aloy": 0.39, "Traveler-A": 0.31, "Dori": 0.26, "Sayu": 0.26, "Amber": 0.25, "Traveler-G": 0.17, "Xinyan": 0.17, "Traveler-E": 0.08
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
                    "cons_usage": {},
                    "cons_avg": appears[phase][char]["cons_avg"],
                    "sample": appears[phase][char]["sample"]
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
                    while i < 20:
                        if i >= len(weapons):
                            uses[phase][char]["weapons"][i] = "-"
                        else:
                            uses[phase][char]["weapons"][weapons[i]] = appears[phase][char]["weap_freq"][weapons[i]]
                        i += 1

                    artifacts = list(appears[phase][char]["arti_freq"])
                    i = 0
                    while i < 20:
                        if i >= len(artifacts):
                            uses[phase][char]["artifacts"][i] = "-"
                        else:
                            uses[phase][char]["artifacts"][artifacts[i]] = appears[phase][char]["arti_freq"][artifacts[i]]
                        i += 1

                    for i in range (7):
                        if owns[phase][char]["cons_freq"][i]["flat"] > 15:
                            uses[phase][char]["cons_usage"][i]["app"] = appears[phase][char]["cons_freq"][i]["percent"]
                            uses[phase][char]["cons_usage"][i]["own"] = owns[phase][char]["cons_freq"][i]["percent"]
                            if char in {"Traveler-A", "Traveler-G", "Traveler-E", "Traveler-D"}:
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
