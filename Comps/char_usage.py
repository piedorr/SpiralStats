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
        "Zhongli": 77.36, "Nahida": 69.98, "Bennett": 68.47, "Yelan": 67.84, "Raiden Shogun": 61.57, "Sangonomiya Kokomi": 57.9, "Kaedehara Kazuha": 57.44, "Xingqiu": 54.64, "Xiangling": 37.49, "Albedo": 36.61, "Alhaitham": 34.1, "Arataki Itto": 33.8, "Yae Miko": 32.32, "Nilou": 30.63, "Hu Tao": 29.97, "Kuki Shinobu": 28.92, "Kamisato Ayato": 27.26, "Fischl": 23.71, "Wanderer": 19.66, "Kamisato Ayaka": 19.35, "Tartaglia": 18.09, "Ganyu": 17.58, "Shenhe": 17.19, "Yoimiya": 15.52, "Gorou": 14.72, "Cyno": 14.53, "Kujou Sara": 13.44, "Xiao": 12.52, "Faruzan": 12.12, "Jean": 10.98, "Yaoyao": 10.04, "Traveler-D": 9.32, "Ningguang": 9.03, "Yun Jin": 8.35, "Eula": 7.58, "Sucrose": 7.14, "Keqing": 6.95, "Noelle": 6.57, "Diona": 6.51, "Mona": 6.03, "Venti": 5.13, "Tighnari": 5.11, "Rosaria": 4.75, "Barbara": 4.56, "Collei": 4.02, "Klee": 3.98, "Beidou": 3.08, "Layla": 2.91, "Traveler-A": 2.41, "Thoma": 1.83, "Qiqi": 1.25, "Yanfei": 1.01, "Lisa": 0.85, "Diluc": 0.67, "Shikanoin Heizou": 0.67, "Razor": 0.6, "Kaeya": 0.55, "Chongyun": 0.47, "Sayu": 0.46, "Traveler-G": 0.45, "Dori": 0.31, "Xinyan": 0.3, "Candace": 0.25, "Amber": 0.15, "Aloy": 0.0, "Traveler-E": 0.0
    }
    past_usage_11 = {
        "Nahida": 71.54, "Kaedehara Kazuha": 71.43, "Bennett": 63.01, "Yelan": 62.07, "Sangonomiya Kokomi": 59.46, "Zhongli": 58.27, "Raiden Shogun": 53.45, "Xingqiu": 51.78, "Wanderer": 39.97, "Kamisato Ayato": 36.3, "Yae Miko": 33.43, "Nilou": 31.48, "Xiangling": 30.68, "Venti": 29.61, "Fischl": 28.22, "Tartaglia": 27.84, "Kuki Shinobu": 24.27, "Kamisato Ayaka": 23.93, "Shenhe": 22.01, "Faruzan": 21.13, "Ganyu": 20.38, "Hu Tao": 18.58, "Albedo": 17.51, "Xiao": 17.16, "Yoimiya": 16.61, "Alhaitham": 13.33, "Sucrose": 13.02, "Arataki Itto": 11.11, "Cyno": 11.05, "Mona": 10.92, "Jean": 10.53, "Tighnari": 10.1, "Traveler-D": 9.67, "Kujou Sara": 9.44, "Diona": 9.23, "Rosaria": 8.69, "Keqing": 7.95, "Eula": 7.84, "Beidou": 7.56, "Yun Jin": 5.79, "Yaoyao": 5.76, "Gorou": 5.11, "Barbara": 4.96, "Collei": 4.82, "Layla": 4.03, "Thoma": 3.81, "Traveler-A": 2.71, "Klee": 2.27, "Shikanoin Heizou": 2.19, "Ningguang": 1.97, "Noelle": 1.8, "Kaeya": 1.65, "Qiqi": 1.36, "Diluc": 1.35, "Lisa": 1.3, "Chongyun": 1.09, "Candace": 1.0, "Sayu": 0.91, "Yanfei": 0.75, "Dori": 0.61, "Razor": 0.45, "Traveler-G": 0.3, "Xinyan": 0.3, "Aloy": 0.17, "Amber": 0.15, "Traveler-E": 0.0
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
