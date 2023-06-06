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

def appearances(players, owns, archetype, chambers=ROOMS, offset=3, info_char=False):
    appears = {}
    num_players = {}
    players_chars = {}
    pyroChars = ["Bennett","Xiangling","Hu Tao","Thoma","Yoimiya","Yanfei","Xinyan","Diluc","Amber","Klee"]
    hydroChars = ["Mona","Sangonomiya Kokomi","Barbara","Xingqiu","Nilou","Candace","Yelan","Kamisato Ayato","Tartaglia"]
    dendroChars = ["Alhaitham","Collei","Nahida","Tighnari","Traveler-D","Yaoyao","Baizhu","Kaveh","Kirara"]
    onField = ["Alhaitham", "Arataki Itto", "Cyno", "Dehya", "Diluc", "Eula", "Ganyu", "Hu Tao", "Kamisato Ayaka", "Kamisato Ayato", "Keqing", "Klee", "Ningguang", "Noelle", "Razor", "Shikanoin Heizou", "Tartaglia", "Tighnari", "Wanderer", "Xiao", "Yanfei", "Yoimiya","Kaveh"]

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

                    foundPyro = False
                    foundHydro = False
                    foundNilou = False
                    foundOnField = False
                    foundDendro = False

                    testChar = 0
                    while not foundPyro and testChar < len(pyroChars):
                        if player.chambers[chamber].char_presence[pyroChars[testChar]]:
                            foundPyro = True
                        testChar += 1

                    testChar = 0
                    while not foundDendro and testChar < len(dendroChars):
                        if player.chambers[chamber].char_presence[dendroChars[testChar]]:
                            foundDendro = True
                        testChar += 1

                    testChar = 0
                    while not foundHydro and testChar < len(hydroChars):
                        if player.chambers[chamber].char_presence[hydroChars[testChar]]:
                            foundHydro = True
                        testChar += 1

                    testChar = 0
                    while not foundOnField and testChar < len(onField):
                        if player.chambers[chamber].char_presence[onField[testChar]]:
                            foundOnField = True
                        testChar += 1

                    if player.chambers[chamber].char_presence["Nilou"]:
                        foundNilou = True

                    isValidChar = False
                    match archetype:
                        case "Nilou":
                            if player.chambers[chamber].char_presence[char] and foundNilou:
                                isValidChar = True
                        case "dendro":
                            if player.chambers[chamber].char_presence[char] and foundDendro:
                                isValidChar = True
                        case "nondendro":
                            if player.chambers[chamber].char_presence[char] and not foundDendro:
                                isValidChar = True
                        case "off-field":
                            if player.chambers[chamber].char_presence[char] and not foundOnField and not foundNilou:
                                isValidChar = True
                        case "on-field":
                            if player.chambers[chamber].char_presence[char] and foundOnField and not foundNilou:
                                isValidChar = True
                        case "melt":
                            if player.chambers[chamber].char_presence[char] and foundPyro:
                                isValidChar = True
                        case "freeze":
                            if player.chambers[chamber].char_presence[char] and not foundPyro and foundHydro:
                                isValidChar = True
                        case _:
                            if player.chambers[chamber].char_presence[char]:
                                isValidChar = True

                    if isValidChar:
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
        "Nahida": 88.61, "Yelan": 82.37, "Sangonomiya Kokomi": 62.64, "Raiden Shogun": 60.73, "Nilou": 59.95, "Kaedehara Kazuha": 58.73, "Bennett": 58.49, "Xingqiu": 56.69, "Baizhu": 54.54, "Zhongli": 47.16, "Alhaitham": 42.39, "Xiangling": 38.29, "Kuki Shinobu": 37.07, "Hu Tao": 25.07, "Yae Miko": 24.83, "Kamisato Ayato": 20.17, "Fischl": 19.41, "Kamisato Ayaka": 18.73, "Yaoyao": 17.64, "Shenhe": 16.81, "Tartaglia": 16.18, "Traveler-D": 11.96, "Cyno": 11.42, "Kujou Sara": 11.08, "Ganyu": 11.01, "Arataki Itto": 10.33, "Albedo": 9.92, "Tighnari": 8.81, "Yoimiya": 7.22, "Wanderer": 7.19, "Dehya": 6.62, "Kirara": 6.57, "Eula": 6.36, "Barbara": 5.64, "Diona": 5.34, "Collei": 5.15, "Xiao": 5.14, "Mona": 4.62, "Keqing": 4.25, "Venti": 4.22, "Jean": 4.13, "Gorou": 4.1, "Faruzan": 4.08, "Sucrose": 3.51, "Kaveh": 3.44, "Beidou": 2.42, "Klee": 2.33, "Rosaria": 2.21, "Yun Jin": 1.94, "Thoma": 1.91, "Layla": 1.66, "Noelle": 1.28, "Candace": 1.27, "Mika": 0.72, "Diluc": 0.66, "Qiqi": 0.57, "Razor": 0.54, "Shikanoin Heizou": 0.52, "Yanfei": 0.52, "Kaeya": 0.43, "Lisa": 0.37, "Ningguang": 0.37, "Chongyun": 0.35, "Amber": 0.34, "Sayu": 0.2, "Traveler-E": 0.17, "Xinyan": 0.17, "Traveler-G": 0.11, "Dori": 0.09, "Traveler-A": 0.09, "Aloy": 0.03
    }
    past_usage_11 = {
        "Nahida": 85.22, "Kaedehara Kazuha": 63.63, "Yelan": 63.07, "Sangonomiya Kokomi": 61.05, "Baizhu": 60.06, "Nilou": 55.4, "Zhongli": 49.79, "Bennett": 49.34, "Xingqiu": 48.99, "Alhaitham": 45.81, "Raiden Shogun": 44.23, "Kuki Shinobu": 34.8, "Yae Miko": 32.7, "Shenhe": 30.58, "Kamisato Ayaka": 29.83, "Ganyu": 28.99, "Xiangling": 28.38, "Kamisato Ayato": 20.33, "Yaoyao": 18.2, "Fischl": 17.78, "Venti": 16.3, "Tartaglia": 15.93, "Hu Tao": 15.82, "Wanderer": 15.75, "Yoimiya": 12.77, "Tighnari": 12.6, "Traveler-D": 11.87, "Cyno": 11.62, "Albedo": 10.33, "Mona": 9.26, "Diona": 8.79, "Dehya": 8.42, "Eula": 7.83, "Barbara": 6.32, "Kaveh": 6.31, "Xiao": 5.95, "Faruzan": 5.86, "Kujou Sara": 5.42, "Arataki Itto": 5.35, "Keqing": 4.78, "Rosaria": 4.74, "Jean": 4.29, "Collei": 4.1, "Sucrose": 3.94, "Beidou": 3.65, "Layla": 3.55, "Yun Jin": 3.13, "Gorou": 2.68, "Klee": 2.67, "Thoma": 2.52, "Mika": 1.85, "Kirara": 1.77, "Noelle": 1.28, "Candace": 1.23, "Diluc": 1.22, "Shikanoin Heizou": 1.19, "Kaeya": 1.02, "Qiqi": 0.95, "Ningguang": 0.94, "Lisa": 0.88, "Yanfei": 0.78, "Chongyun": 0.7, "Razor": 0.51, "Amber": 0.26, "Dori": 0.26, "Xinyan": 0.26, "Aloy": 0.2, "Sayu": 0.17, "Traveler-A": 0.09, "Traveler-G": 0.09, "Traveler-E": 0.09
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
