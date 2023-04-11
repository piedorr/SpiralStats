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
    pyroChars = ["Bennett","Xiangling","Hu Tao","Thoma","Yoimiya","Yanfei","Xinyan","Diluc","Amber","Klee"]
    hydroChars = ["Mona","Sangonomiya Kokomi","Barbara","Xingqiu","Nilou","Candace","Yelan","Kamisato Ayato","Tartaglia"]
    onField = ["Alhaitham", "Arataki Itto", "Cyno", "Dehya", "Diluc", "Eula", "Ganyu", "Hu Tao", "Kamisato Ayaka", "Kamisato Ayato", "Keqing", "Klee", "Ningguang", "Noelle", "Razor", "Shikanoin Heizou", "Tartaglia", "Tighnari", "Wanderer", "Xiao", "Yanfei", "Yoimiya"]

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
                    # foundOnField = False

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

                    # testChar = 0
                    # while not foundOnField and testChar < len(onField):
                    #     if player.chambers[chamber].char_presence[onField[testChar]]:
                    #         foundOnField = True
                    #     testChar += 1

                    # if player.chambers[chamber].char_presence["Nilou"]:
                    #     foundNilou = True

                    # if player.chambers[chamber].char_presence[char] and not foundPyro and foundHydro:
                    # if player.chambers[chamber].char_presence[char] and not foundOnField and not foundNilou:
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
        "Nahida": 77.86, "Bennett": 76.73, "Yelan": 72.7, "Kaedehara Kazuha": 68.8, "Xingqiu": 67.63, "Raiden Shogun": 60.08, "Xiangling": 59.26, "Zhongli": 48.32, "Alhaitham": 43.79, "Hu Tao": 43.02, "Yae Miko": 38.46, "Sangonomiya Kokomi": 38.06, "Kuki Shinobu": 34.63, "Kamisato Ayaka": 27.59, "Dehya": 26.13, "Shenhe": 25.99, "Tartaglia": 23.07, "Kamisato Ayato": 19.0, "Ganyu": 18.2, "Yoimiya": 16.79, "Fischl": 15.82, "Tighnari": 13.03, "Nilou": 12.93, "Mona": 11.02, "Diona": 9.1, "Albedo": 8.81, "Yaoyao": 8.33, "Sucrose": 8.09, "Xiao": 7.59, "Arataki Itto": 7.22, "Cyno": 6.89, "Wanderer": 6.77, "Jean": 6.74, "Eula": 6.1, "Kujou Sara": 5.55, "Faruzan": 5.38, "Venti": 5.03, "Keqing": 4.98, "Klee": 4.5, "Rosaria": 4.5, "Traveler-D": 4.33, "Thoma": 3.36, "Gorou": 2.94, "Yun Jin": 2.7, "Layla": 2.64, "Barbara": 2.36, "Diluc": 1.93, "Yanfei": 1.69, "Kaeya": 1.35, "Beidou": 1.2, "Collei": 0.87, "Noelle": 0.87, "Lisa": 0.63, "Chongyun": 0.59, "Amber": 0.53, "Razor": 0.48, "Sayu": 0.48, "Xinyan": 0.44, "Shikanoin Heizou": 0.42, "Ningguang": 0.34, "Qiqi": 0.32, "Dori": 0.29, "Traveler-A": 0.1, "Traveler-G": 0.1, "Aloy": 0.0, "Candace": 0.0, "Traveler-E": 0.0
    }
    past_usage_11 = {
        "Kaedehara Kazuha": 72.62, "Nahida": 71.49, "Zhongli": 65.19, "Bennett": 64.74, "Yelan": 59.39, "Xingqiu": 51.23, "Raiden Shogun": 47.28, "Sangonomiya Kokomi": 46.32, "Dehya": 44.14, "Hu Tao": 43.46, "Shenhe": 42.86, "Xiangling": 42.42, "Alhaitham": 39.61, "Kamisato Ayaka": 37.28, "Ganyu": 34.31, "Yae Miko": 31.07, "Kuki Shinobu": 28.27, "Yoimiya": 23.38, "Nilou": 19.59, "Fischl": 17.42, "Kamisato Ayato": 16.85, "Tartaglia": 16.72, "Diona": 14.4, "Wanderer": 13.53, "Venti": 12.49, "Tighnari": 12.4, "Albedo": 12.37, "Yaoyao": 11.94, "Cyno": 10.8, "Sucrose": 9.3, "Mona": 9.19, "Rosaria": 8.56, "Eula": 8.54, "Xiao": 8.54, "Faruzan": 7.96, "Traveler-D": 6.2, "Arataki Itto": 5.99, "Keqing": 5.79, "Jean": 5.66, "Kujou Sara": 5.5, "Layla": 4.84, "Yun Jin": 4.27, "Diluc": 3.85, "Klee": 3.78, "Beidou": 3.46, "Thoma": 3.36, "Kaeya": 2.89, "Gorou": 2.52, "Yanfei": 2.03, "Barbara": 1.73, "Chongyun": 1.62, "Qiqi": 1.62, "Collei": 1.44, "Noelle": 1.01, "Shikanoin Heizou": 0.79, "Lisa": 0.58, "Ningguang": 0.58, "Amber": 0.43, "Sayu": 0.43, "Razor": 0.29, "Xinyan": 0.29, "Candace": 0.21, "Aloy": 0.0, "Dori": 0.0, "Traveler-A": 0.0, "Traveler-G": 0.0, "Traveler-E": 0.0
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
