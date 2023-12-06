import json
import pandas as pd
import operator
import statistics
from numpy import quantile
from matplotlib import pyplot as plt
from scipy.stats import skew, trim_mean
from archetypes import *

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
            for character in players[phase][player].owned.keys():
                owns[phase][character]["flat"] += 1
                owns[phase][character]["cons_freq"][
                    players[phase][player].owned[character]["cons"]
                ]["flat"] += 1
        total /= 100.0
        for char in owns[phase]:
            own_flat = owns[phase][char]["flat"] / 100.0
            if own_flat > 0:
                if "Traveler" in char:
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
                "flat_1": 0,
                "flat_2": 0,
                "duration": {"1-1": [], "1-2": [], "2-1": [], "2-2": [], "3-1": []},
                "avg_duration": 0.00,
                "avg_duration_2": 0.00,
                "percent": 0.00,
                "weap_freq": {},
                "weap_duration": {},
                "arti_freq": {},
                "arti_duration": {},
                "cons_freq": {},
                "cons_avg": 0.00,
                "sample": 0
            }
            for i in range (7):
                appears[phase][character]["cons_freq"][i] = {
                    "flat": 0,
                    "duration": {"1-1": [], "1-2": [], "2-1": [], "2-2": [], "3-1": []},
                    "avg_duration": 0.00,
                    "percent": 0,
                }

        # There's probably a better way to cache these things
        for player in players[phase].values():
            num_players[phase] += 1
            for chamber in chambers:
                if player.chambers[chamber] == None:
                    continue
                foundchar = resetfind()
                whaleComp = False
                for char in player.chambers[chamber].characters:
                    findchars(char, foundchar)
                    if CHARACTERS[char]["availability"] in ["Limited 5*"]:
                        if player.owned[char]["cons"] > 1:
                            whaleComp = True
                if find_archetype(foundchar):
                    for char in player.chambers[chamber].characters:
                        # to print the amount of players using a character, for char infographics
                        if player.player not in players_chars[phase][char]:
                            players_chars[phase][char].append(player.player)

                        char_name = char
                        appears[phase][char_name]["flat"] += 1
                        if chamber[-1:] == "1":
                            appears[phase][char_name]["flat_1"] += 1
                        else:
                            appears[phase][char_name]["flat_2"] += 1
                        # In case of character in comp data missing from character data
                        if char not in player.owned:
                            print("Comp data missing from character data: " + str(player.player) + ", " + str(char))
                            if player.player not in error_comps:
                                error_comps.append(player.player)
                            comp_error = True
                            continue
                        if player.chambers[chamber].duration and not whaleComp:
                            appears[phase][char_name]["duration"][chamber[-3:]].append(player.chambers[chamber].duration)
                        appears[phase][char_name]["cons_freq"][player.owned[char]["cons"]]["flat"] += 1
                        if player.chambers[chamber].duration:
                            appears[phase][char_name]["cons_freq"][player.owned[char]["cons"]]["duration"][chamber[-3:]].append(player.chambers[chamber].duration)
                        appears[phase][char_name]["cons_avg"] += player.owned[char]["cons"]

                        if player.owned[char]["weapon"] != "":
                            if player.owned[char]["weapon"] not in appears[phase][char_name]["weap_freq"]:
                                appears[phase][char_name]["weap_freq"][player.owned[char]["weapon"]] = 0
                                appears[phase][char_name]["weap_duration"][player.owned[char]["weapon"]] = {"1-1": [], "1-2": [], "2-1": [], "2-2": [], "3-1": []}
                            appears[phase][char_name]["weap_freq"][player.owned[char]["weapon"]] += 1
                            if player.chambers[chamber].duration and not whaleComp:
                                appears[phase][char_name]["weap_duration"][player.owned[char]["weapon"]][chamber[-3:]].append(player.chambers[chamber].duration)

                        if player.owned[char]["artifacts"] != "":
                            if player.owned[char]["artifacts"] not in appears[phase][char_name]["arti_freq"]:
                                appears[phase][char_name]["arti_freq"][player.owned[char]["artifacts"]] = 0
                                appears[phase][char_name]["arti_duration"][player.owned[char]["artifacts"]] = {"1-1": [], "1-2": [], "2-1": [], "2-2": [], "3-1": []}
                            appears[phase][char_name]["arti_freq"][player.owned[char]["artifacts"]] += 1
                            if player.chambers[chamber].duration and not whaleComp:
                                appears[phase][char_name]["arti_duration"][player.owned[char]["artifacts"]][chamber[-3:]].append(player.chambers[chamber].duration)

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
            # if appears[phase][char]["flat"] > 0:
            #     appears[phase][char]["flat_1"] /= appears[phase][char]["flat"]
            #     appears[phase][char]["flat_2"] /= appears[phase][char]["flat"]

            all_duration = []
            all_duration_1 = []
            all_duration_2 = []
            for room_num in appears[phase][char]["duration"]:
                all_duration.extend(appears[phase][char]["duration"][room_num])
                if room_num[-1:] == "1":
                    all_duration_1.extend(appears[phase][char]["duration"][room_num])
                else:
                    all_duration_2.extend(appears[phase][char]["duration"][room_num])

            avg_duration = {"1": [], "2": []}
            for room_num in appears[phase][char]["duration"]:
                if appears[phase][char]["duration"][room_num]:
                    # if len(all_duration_1) >= 15:
                    #     print(appears[phase][char]["duration"][room_num])
                    #     print(list(filter(
                    #         lambda x: x <= quantile(appears[phase][char]["duration"][room_num], .25), appears[phase][char]["duration"][room_num])))
                    #     exit()
                    avg_duration[room_num[-1:]].append(statistics.mean(list(filter(
                        lambda x: x <= quantile(appears[phase][char]["duration"][room_num], .5), appears[phase][char]["duration"][room_num]))))
                    # skewness = skew(appears[phase][char]["duration"][room_num], axis=0, bias=True)
                    # if abs(skewness) > 0.8:
                    #     avg_duration[room_num[-1:]].append(trim_mean(appears[phase][char]["duration"][room_num], 0.25))
                    # else:
                    #     avg_duration[room_num[-1:]].append(statistics.mean(appears[phase][char]["duration"][room_num]))

            if len(all_duration_1) >= 15 and avg_duration["1"]:
                appears[phase][char]["avg_duration_1"] = round(statistics.mean(avg_duration["1"]), 1)
            else:
                appears[phase][char]["avg_duration_1"] = 999

            if len(all_duration_2) >= 5 and avg_duration["2"]:
                appears[phase][char]["avg_duration_2"] = round(statistics.mean(avg_duration["2"]), 1)
            else:
                appears[phase][char]["avg_duration_2"] = 999

            if (chambers == ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"]):
                # # print("char: " + char)
                # # print("    " + str(len(all_duration)))
                # # print("    " + str(statistics.median(all_duration)))
                # # print("    " + str(statistics.median(all_duration)))
                # try:
                #     if len(all_duration_1) >= 5:
                #         plt.hist(all_duration_1)
                #         plt.title(char + ' - Side 1')
                #         plt.savefig('../char_results/' + char + '1.png')
                #         plt.close()
                #     if len(all_duration_2) >= 5:
                #         plt.hist(all_duration_2)
                #         plt.title(char + ' - Side 2')
                #         plt.savefig('../char_results/' + char + '2.png')
                #         plt.close()
                # except Exception:
                #     pass

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

def usages(owns, appears, past_phase, filename, chambers=ROOMS, offset=3):
    uses = {}

    try:
        with open("../char_results/" + past_phase + "/" + filename + ".csv") as stats:
            # uid_freq_comp will help detect duplicate UIDs
            reader = csv.reader(stats)
            col_names = next(reader)
            past_usage = {}

            # Append lines and check for duplicate UIDs by checking if
            # there are exactly 12 entries (1 for each chamber) for a UID
            for line in reader:
                past_usage[line[0]] = float(line[1].strip('%'))
    except:
        past_usage = {}

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
                    "duration_1": appears[phase][char]["avg_duration_1"],
                    "duration_2": appears[phase][char]["avg_duration_2"],
                    "own": owns[phase][char]["percent"],
                    "usage" : rate,
                    "diff": "-",
                    "role": CHARACTERS[char]["role"],
                    "rarity": CHARACTERS[char]["availability"],
                    "weapons" : {},
                    "artifacts" : {},
                    "cons_usage": {},
                    "cons_avg": appears[phase][char]["cons_avg"],
                    "sample": appears[phase][char]["sample"]
                }

                if char in past_usage:
                    uses[phase][char]["diff"] = round(rate - past_usage[char], 2)

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
                            if "Traveler" in char:
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
