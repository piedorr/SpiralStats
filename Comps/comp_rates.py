import csv
import json
import os.path
import operator
import char_usage as cu
import statistics
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from itertools import permutations
from composition import Composition
from player_phase import PlayerPhase
from comp_rates_config import *
from archetypes import *

def main():
    for make_path in [
        "../comp_results", "../enka.network/results",
        "../char_results"
    ]:
        if not os.path.exists(make_path):
            os.makedirs(make_path)

    # Sample size will be needed to calculate the comp app and own rate
    global sample_size
    sample_size = 0
    print("start")

    global comps_list
    comps_list = []
    reader = csv.reader(open("../data/comps_list.csv"))
    for line in reader:
        comps_list.append(tuple(line))

    if os.path.exists("../data/raw_csvs_real/"):
        stats = open("../data/raw_csvs_real/" + RECENT_PHASE + "_char.csv")
    else:
        stats = open("../data/raw_csvs/" + RECENT_PHASE + "_char.csv")

    reader = csv.reader(stats)
    col_names = next(reader)
    player_table = []

    # uid_freq_char and last_uid will help detect duplicate UIDs
    # trav_elements stores the elements of the traveler of all players
    uid_freq_char = []
    trav_elements = {}
    last_uid = "0"

    # Append lines
    for line in reader:
        line[1] = RECENT_PHASE
        # Change traveler's name to respective element
        if line[2] == "Traveler":
            if line[7] == "Geo":
                line[2] = "Traveler-G"
            elif line[7] == "Anemo":
                line[2] = "Traveler-A"
            elif line[7] == "Electro":
                line[2] = "Traveler-E"
            elif line[7] == "Dendro":
                line[2] = "Traveler-D"
            elif line[7] == "Hydro":
                line[2] = "Traveler-H"
            elif line[7] == "Pyro":
                line[2] = "Traveler-P"
            elif line[7] == "Cryo":
                line[2] = "Traveler-C"
            elif line[7] == "None":
                line[2] = "Traveler-D"
            else:
                print(line[7] + line[2])
            trav_elements[line[0]] = line[7]
        player_table.append(line)

        # Check for duplicate UIDs by keeping track of the amount of
        # batches of owned characters for each UID. If a UID has
        # more than two batches of owned characters, it's a duplicate.
        if line[0] != last_uid:
            if line[0] in uid_freq_char:
                print("duplicate UID in char: " + line[0])
            else:
                uid_freq_char.append(line[0])
        last_uid = line[0]


    if os.path.exists("../data/raw_csvs_real/"):
        stats = open("../data/raw_csvs_real/" + RECENT_PHASE + ".csv")
    else:
        stats = open("../data/raw_csvs/" + RECENT_PHASE + ".csv")
    # uid_freq_comp will help detect duplicate UIDs
    reader = csv.reader(stats)
    col_names = next(reader)
    comp_table = []
    uid_freq_comp = {}

    # Append lines and check for duplicate UIDs by checking if
    # there are exactly 12 entries (1 for each chamber) for a UID
    for line in reader:
        if line[0] in uid_freq_comp:
            uid_freq_comp[line[0]] += 1
        else:
            if uid_freq_comp and uid_freq_comp[list(uid_freq_comp)[-1]] < 12:
                print("not enough comps: " + list(uid_freq_comp)[-1])
            uid_freq_comp[line[0]] = 1
        if uid_freq_comp[line[0]] > 12:
            print("duplicate UID in comp: " + line[0])

        # Change traveler to respective element
        for i in range (4,8):
            if "Traveler" in line[i]:
                try:
                    match trav_elements[line[0]]:
                        case "Anemo":
                            line[i] = 'Traveler-A'
                        case "Geo":
                            line[i] = 'Traveler-G'
                        case "Electro":
                            line[i] = 'Traveler-E'
                        case "Dendro":
                            line[i] = 'Traveler-D'
                        case "Hydro":
                            line[i] = 'Traveler-H'
                        case "Pyro":
                            line[i] = 'Traveler-P'
                        case "Cryo":
                            line[i] = 'Traveler-C'
                        # case "None":
                        #     line[col_names.index('Traveler')] = "1"
                        case _:
                            print(trav_elements[line[0]])
                except KeyError:
                    print("Traveler key error: " + line[0])
        comp_table.append(line)
        sample_size += 1
    print("done csv")

    # 12 entries for each UID, so sample size
    # should be divided by 12
    sample_size /= 12
    print("sample size: " + str(sample_size))

    # Check for missing UIDs
    csv_writer = csv.writer(open("../char_results/uids.csv", 'w', newline=''))
    for uid in uid_freq_comp:
        csv_writer.writerow([uid])
        if uid not in uid_freq_char:
            print("comp not in char: " + uid)
    for uid in uid_freq_char:
        if uid not in uid_freq_comp:
            print("char not in comp: " + uid)

    all_comps = form_comps(col_names, comp_table, alt_comps)
    all_players = form_players(player_table, all_comps, [RECENT_PHASE])
    print("done form")

    # Below are the commands to print CSV files, comment the ones not needed

    if "Char usages all chambers" in run_commands:
        global usage
        usage = char_usages(all_players, past_phase, filename="12", floor=True)
        char_usages(all_players, past_phase, filename="12 build", info_char=True, floor=True)
        char_usages(all_players, past_phase, rooms=["11-1-1", "11-1-2", "11-2-1", "11-2-2", "11-3-1", "11-3-2"], filename="11")
        duo_usages(all_comps, all_players, usage)
        print("done char")

    if "Comp usage floor 12 each half" in run_commands:
        comp_usages(all_comps, all_players, rooms=["12-1-2", "12-2-2", "12-3-2"], filename="12 second", floor=True)
        comp_usages(all_comps, all_players, rooms=["12-1-1", "12-2-1", "12-3-1"], filename="12 first", floor=True)
        print("done 12 comps")

    if "Comp usage floor 11 each half" in run_commands:
        comp_usages(all_comps, all_players, rooms=["11-1-2", "11-2-2", "11-3-2"], filename="11 second", floor=True)
        comp_usages(all_comps, all_players, rooms=["11-1-1", "11-2-1", "11-3-1"], filename="11 first", floor=True)
        print("done 11 comps")

    if "Comp usage floor 12 combined" in run_commands:
        comp_usages(all_comps, all_players, rooms=["12-1-2", "12-2-2", "12-3-2", "12-1-1", "12-2-1", "12-3-1"], filename="12", floor=True)
        print("done 12 comps combined")

    if "Comp usage each chamber" in run_commands:
        for room in ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2", "11-1-1", "11-1-2", "11-2-1", "11-2-2", "11-3-1", "11-3-2"]:
            comp_usages(all_comps, all_players, rooms=[room], filename=room, offset=1)
        print("done chamber comps")

    if "Character specific infographics" in run_commands:
        comp_usages(all_comps, all_players, filename=char_infographics, info_char=True, floor=True)
        print("char infographics")

    if "Char usages for each chamber" in run_commands:
        for room in ["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2", "11-1-1", "11-1-2", "11-2-1", "11-2-2", "11-3-1", "11-3-2"]:
            char_usages(all_players, past_phase, rooms=[room], filename=room, offset=1)
        print("done char chambers")

def comp_usages(comps, 
                players, 
                rooms=["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"],
                filename="comp_usages",
                offset=3,
                info_char=False,
                floor=False):
    comps_dict = used_comps(players, comps, rooms, floor=floor)
    comp_owned(players, comps_dict, owns_offset=offset)
    rank_usages(comps_dict, owns_offset=offset)
    comp_usages_write(comps_dict, filename, floor, info_char)

def used_comps(players, comps, rooms, phase=RECENT_PHASE, floor=False):
    # Returns the dictionary of all the comps used and how many times they were used
    comps_dict = {}
    error_uids = []
    # deepwoodTighnari = 0
    # deepwoodEquipChars = {}
    # meltGanyu = 0
    # meltGanyuWeap = {}
    # meltGanyuArti = {}
    # lessFour = []
    # lessFourComps = {}
    totalComps = 0
    whaleCount = 0
    for comp in comps:
        comp_tuple = tuple(comp.characters)
        # Check if the comp is used in the rooms that are being checked
        if comp.room not in rooms or len(comp_tuple) < 4:
            continue

        foundchar = resetfind()
        for char in comp.characters:
            findchars(char, foundchar)
        if find_archetype(foundchar):
            totalComps += 1
            if whaleCheck:
                whaleComp = False
                for char in range (4):
                    if (
                        players[phase][comp.player].owned[comp_tuple[char]]["cons"] != 0
                        and CHARACTERS[comp_tuple[char]]["availability"] in ["Limited 5*"]
                    ) or (
                        whaleSigWeap and players[phase][comp.player].owned[comp_tuple[char]]["weapon"] in sigWeaps
                    ):
                        whaleComp = True
                if whaleComp and not(whaleCheckOnly):
                    whaleCount += 1
                    continue
                elif not(whaleComp) and whaleCheckOnly:
                    continue
            # if len(comp_tuple) < 4:
            #     lessFour.append(comp.player)
            #     continue
            if comp_tuple not in comps_dict:
                comps_dict[comp_tuple] = {
                    "uses": 1,
                    "owns": 0,
                    "5* count": comp.fivecount,
                    "comp_name": comp.comp_name,
                    "alt_comp_name": comp.alt_comp_name,
                    "deepwood": 0,
                    "players": set(),
                }
                if floor:
                    # deepwood = False
                    # melt = False
                    # deepwoodEquip = ""
                    for char in range (4):
                        # if char in ["Thoma","Yoimiya","Yanfei","Hu Tao","Xinyan","Diluc","Amber","Xiangling","Klee","Bennett"]:
                        #     melt = True
                        # "weapon" and "artifacts" stores dictionary of
                        # used gear, key is the name of the gear, value is the app#
                        comps_dict[comp_tuple][comp_tuple[char]] = {
                            "weapon" : {},
                            "artifacts" : {},
                            "cons": []
                        }
                    # if deepwood:
                    #     comps_dict[comp_tuple]["deepwood"] += 1
                    #     if ("Tighnari" in comp_tuple):
                    #         deepwoodTighnari += 1
                    #         if deepwoodEquip in deepwoodEquipChars:
                    #             deepwoodEquipChars[deepwoodEquip] += 1
                    #         else:
                    #             deepwoodEquipChars[deepwoodEquip] = 1
                    # if melt and "Ganyu" in comp_tuple:
                    #     meltGanyu += 1
            else:
                comps_dict[comp_tuple]["uses"] +=1
                if floor:
                    # deepwood = False
                    # deepwoodEquip = ""
                    for i in range(4):
                        try:
                            if players[phase][comp.player].owned[comp_tuple[i]]["weapon"] in comps_dict[comp_tuple][comp_tuple[i]]["weapon"]:
                                comps_dict[comp_tuple][comp_tuple[i]]["weapon"][players[phase][comp.player].owned[comp_tuple[i]]["weapon"]] += 1
                            else:
                                comps_dict[comp_tuple][comp_tuple[i]]["weapon"][players[phase][comp.player].owned[comp_tuple[i]]["weapon"]] = 1
                            if players[phase][comp.player].owned[comp_tuple[i]]["artifacts"] != "":
                                if players[phase][comp.player].owned[comp_tuple[i]]["artifacts"] in comps_dict[comp_tuple][comp_tuple[i]]["artifacts"]:
                                    comps_dict[comp_tuple][comp_tuple[i]]["artifacts"][players[phase][comp.player].owned[comp_tuple[i]]["artifacts"]] += 1
                                else:
                                    comps_dict[comp_tuple][comp_tuple[i]]["artifacts"][players[phase][comp.player].owned[comp_tuple[i]]["artifacts"]] = 1
                                # if players[phase][comp.player].owned[comp_tuple[i]]["artifacts"] == "Deepwood Memories":
                                #     deepwood = True
                                #     deepwoodEquip = comp_tuple[i]
                        except Exception as e:
                            if ('{}: {}'.format(comp.player, e)) not in error_uids:
                                error_uids.append('{}: {}'.format(comp.player, e))
                    # if deepwood:
                    #     comps_dict[comp_tuple]["deepwood"] += 1
                    #     if ("Tighnari" in comp_tuple):
                    #         deepwoodTighnari += 1
                    #         if deepwoodEquip in deepwoodEquipChars:
                    #             deepwoodEquipChars[deepwoodEquip] += 1
                    #         else:
                    #             deepwoodEquipChars[deepwoodEquip] = 1
            comps_dict[comp_tuple]["players"].add(comp.player)
    if floor:
        for comp in comps_dict:
            for char in comp:
                sorted_weapons = (sorted(
                    comps_dict[comp][char]["weapon"].items(),
                    key = operator.itemgetter(1),
                    reverse=True
                ))
                if(len(sorted_weapons) > 1):
                    maxWeapon = sorted_weapons[0][1]
                    sortWeapons = [sorted_weapons[0]]
                    for i in range (1, len(sorted_weapons)):
                        if sorted_weapons[i][1] == maxWeapon:
                            # print(i)
                            # print(sorted_weapons)
                            # print(maxWeapon)
                            sortWeapons.append(sorted_weapons[i])
                        else:
                            break
                    if len(sortWeapons) > 1:
                        foundWeapon = False
                        # print()
                        # print(list(usage[RECENT_PHASE][char]["weapons"]))
                        # print(sorted_weapons)
                        for charWeapon in (list(usage[RECENT_PHASE][char]["weapons"])):
                            for compCharWeapon in sortWeapons:
                                if compCharWeapon[0] == charWeapon:
                                    foundWeapon = True
                                    maxWeapon = compCharWeapon
                            if foundWeapon:
                                break
                        if not(foundWeapon):
                            print(char)
                            print(list(usage[RECENT_PHASE][char]["weapons"]))
                            print(sorted_weapons)
                        if foundWeapon:
                            sorted_weapons.remove(maxWeapon)
                            sorted_weapons.insert(0, maxWeapon)
                        # print(sorted_weapons)
                comps_dict[comp][char]["weapon"] = {k: v for k, v in sorted_weapons}

                sorted_artifacts = (sorted(
                    comps_dict[comp][char]["artifacts"].items(),
                    key = operator.itemgetter(1),
                    reverse=True
                ))
                if(len(sorted_artifacts) > 1):
                    maxArtifact = sorted_artifacts[0][1]
                    sortArtifacts = [sorted_artifacts[0]]
                    for i in range (1, len(sorted_artifacts)):
                        if sorted_artifacts[i][1] == maxArtifact:
                            # print(i)
                            # print(sorted_artifacts)
                            # print(maxArtifact)
                            sortArtifacts.append(sorted_artifacts[i])
                        else:
                            break
                    if len(sortArtifacts) > 1:
                        foundArtifact = False
                        # print()
                        # print(list(usage[RECENT_PHASE][char]["artifacts"]))
                        # print(sorted_artifacts)
                        for charArtifact in (list(usage[RECENT_PHASE][char]["artifacts"])):
                            for compCharArtifact in sortArtifacts:
                                if compCharArtifact[0] == charArtifact:
                                    foundArtifact = True
                                    maxArtifact = compCharArtifact
                            if foundArtifact:
                                break
                        if not(foundArtifact):
                            print(char)
                            print(list(usage[RECENT_PHASE][char]["artifacts"]))
                            print(sorted_artifacts)
                        if foundArtifact:
                            sorted_artifacts.remove(maxArtifact)
                            sorted_artifacts.insert(0, maxArtifact)
                        # print(sorted_artifacts)
                comps_dict[comp][char]["artifacts"] = {k: v for k, v in sorted_artifacts}
    # print("Less than four: " + str(lessFour))
    # print("Less than four: " + str(len(lessFour)/totalComps))
    if whaleCheck and not(whaleCheckOnly):
        print("Whale percentage: " + str(whaleCount/totalComps))
    # print("Tighnari with deepwood: " + str(deepwoodTighnari))
    # print(deepwoodEquipChars)
    return comps_dict

def comp_owned(players, comps_dict, phase=RECENT_PHASE, owns_offset=3):
    # For every comp that is used, calculate the ownership rate,
    # i.e. how many players own all four characters in the comp
    for player in players[phase].values():
        for comp in comps_dict:
            if player.chars_owned(comp):
                if whaleCheck:
                    whaleComp = False
                    for char in comp:
                        if char not in CHARACTERS:
                            continue
                        if char not in player.owned:
                            if whaleSigWeap:
                                for trav in ["Traveler-G", "Traveler-A", "Traveler-E", "Traveler-D", "Traveler-H", "Traveler-P", "Traveler-C"]:
                                    if trav in player.owned:
                                        if player.owned[trav]["weapon"] in sigWeaps:
                                            whaleComp = True
                                            break
                            continue
                        if (
                            player.owned[char]["cons"] != 0
                            and CHARACTERS[char]["availability"] in ["Limited 5*"]
                        ) or (
                            whaleSigWeap and player.owned[char]["weapon"] in sigWeaps
                        ):
                            whaleComp = True
                    if whaleComp and not(whaleCheckOnly):
                        continue
                    elif not(whaleComp) and whaleCheckOnly:
                        continue
                comps_dict[comp]["owns"] += owns_offset

def rank_usages(comps_dict, owns_offset=3):
    # Calculate the usage rate and sort the comps according to it
    rates = []
    for comp in comps_dict:
        rate = int(100.0 * comps_dict[comp]["uses"] / comps_dict[comp]["owns"] * 100 + .5) / 100.0
        comps_dict[comp]["usage_rate"] = rate
        app = int(100.0 * comps_dict[comp]["uses"] / (sample_size * owns_offset) * 100 + .5) / 100.0
        comps_dict[comp]["app_rate"] = app
        own = int(100.0 * comps_dict[comp]["owns"] / (sample_size * owns_offset) * 100 + .5) / 100.0
        comps_dict[comp]["own_rate"] = own
        deepwood = int(100.0 * comps_dict[comp]["deepwood"] / comps_dict[comp]["uses"] * 100 + .5) / 100.0
        comps_dict[comp]["deepwood_rate"] = deepwood
        rates.append(rate)
    rates.sort(reverse=True)
    for comp in comps_dict:
        comps_dict[comp]["usage_rank"] = rates.index(comps_dict[comp]["usage_rate"]) + 1

    # # To check the list of weapons and artifacts for a comp
    # comp_tuple = ("Tighnari","Yae Miko","Fischl","Zhongli")
    # print(comp_tuple)
    # print("   App: " + str(comps_dict[comp_tuple]["app_rate"]))
    # print("   Own: " + str(comps_dict[comp_tuple]["own_rate"]))
    # print("   Usage: " + str(comps_dict[comp_tuple]["usage_rate"]))
    # print("   5* Count: " + str(comps_dict[comp_tuple]["5* count"]))
    # print("   Deepwood Holders: " + str(comps_dict[comp_tuple]["deepwood"]))
    # print("   Deepwood Rate: " + str(comps_dict[comp_tuple]["deepwood_rate"]))
    # if comps_dict[comp_tuple]["5* count"] <= 1:
    #     print("   F2P App: " + str(comps_dict[comp_tuple]["app_rate"]))
    # print()
    # for i in comp_tuple:
    #     print(i + ": ")
    #     for weapon in comps_dict[comp_tuple][i]["weapon"]:
    #         print("   " + weapon + ": " + str(comps_dict[comp_tuple][i]["weapon"][weapon]))
    #     print()
    #     for artifacts in comps_dict[comp_tuple][i]["artifacts"]:
    #         print("   " + artifacts + ": " + str(comps_dict[comp_tuple][i]["artifacts"][artifacts]))
    #     print()

def duo_usages(comps,
                players,
                usage,
                rooms=["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"],
                filename="duo_usages"):
    duos_dict = used_duos(players, comps, rooms, usage)
    duo_write(duos_dict, usage, filename)

def used_duos(players, comps, rooms, usage, phase=RECENT_PHASE):
    # Returns dictionary of all the duos used and how many times they were used
    duos_dict = {}

    for comp in comps:
        if len(comp.characters) < 2 or comp.room not in rooms:
            continue

        foundchar = resetfind()
        for char in comp.characters:
            findchars(char, foundchar)
        if not find_archetype(foundchar):
            continue

        # Permutate the duos, for example if Ganyu and Xiangling are used,
        # two duos are used, Ganyu/Xiangling and Xiangling/Ganyu
        duos = list(permutations(comp.characters, 2))
        for duo in duos:
            if duo not in duos_dict:
                duos_dict[duo] = 1
            else:
                duos_dict[duo] += 1

    sorted_duos = (sorted(
        duos_dict.items(),
        key = operator.itemgetter(1),
        reverse=True
    ))
    duos_dict = {k: v for k, v in sorted_duos}

    sorted_duos = {}
    for duo in duos_dict:
        if usage[phase][duo[0]]["app_flat"] > 0:
            # Calculate the appearance rate of the duo by dividing the appearance count
            # of the duo with the appearance count of the first character
            duos_dict[duo] = round (duos_dict[duo] * 100 / usage[phase][duo[0]]["app_flat"], 2)
            if duo[0] not in sorted_duos:
                sorted_duos[duo[0]] = []
            sorted_duos[duo[0]].append([duo[1], duos_dict[duo]])

    return sorted_duos

def char_usages(players,
                past_phase,
                rooms=["12-1-1", "12-1-2", "12-2-1", "12-2-2", "12-3-1", "12-3-2"],
                filename="char_usages",
                offset=3,
                info_char=False,
                floor=False):
    own = cu.ownership(players, chambers = rooms)
    app = cu.appearances(players, own, chambers = rooms, offset = offset, info_char = info_char)
    chars_dict = cu.usages(own, app, past_phase, filename, chambers = rooms, offset = offset)
    # # Print the list of weapons and artifacts used for a character
    # if floor:
    #     print(app[RECENT_PHASE][filename])
    char_usages_write(chars_dict[RECENT_PHASE], filename, floor)
    return chars_dict

def comp_usages_write(comps_dict, filename, floor, info_char):
    out_json = []
    out_comps = []
    outvar_comps = []
    var_comps = []

    # Sort the comps according to their usage rate
    comps_dict = dict(sorted(comps_dict.items(), key=lambda t: t[1]["usage_rate"], reverse=True))
    comps_list_csv_writer = csv.writer(open("../data/comps_list.csv", 'a', newline=''))

    # # A separate dictionary is used for the F2P comps,
    # # which sorts the comps according to their appearance rate
    # f2p_comps_dict = dict(sorted(comps_dict.items(), key=lambda t: t[1]["app_rate"], reverse=True))
    # if floor and not info_char:
    #     f2p_comps = []
    #     comp_names = []
    #     for comp in f2p_comps_dict:
    #         comp_name = f2p_comps_dict[comp]["comp_name"]
    #         # Only one variation of each comp name is included
    #         if (
    #             f2p_comps_dict[comp]["5* count"] <= 1
    #             and (comp_name not in comp_names or comp_name == "-")
    #             and f2p_comps_dict[comp]["app_rate"] > f2p_app_rate_threshold
    #         ):
    #             if comp not in comps_list:
    #                 add_comp_list = input("Input " + str(comp) + " / " + comp_name + "? (y/n)")
    #                 if add_comp_list == "y":
    #                     comps_list_csv_writer.writerow(comp)
    #             comp_names.append(comp_name)
    #             if f2p_comps_dict[comp]["alt_comp_name"] != "-":
    #                 comp_name = f2p_comps_dict[comp]["alt_comp_name"]
    #             f2p_comps_append = {
    #                 "comp_name": comp_name,
    #                 "char_one": comp[0],
    #                 "char_two": comp[1],
    #                 "char_three": comp[2],
    #                 "char_four": comp[3],
    #                 "app_rate": str(f2p_comps_dict[comp]["app_rate"]) + "%"
    #             }
    #             j = 1
    #             for i in comp:
    #                 f2p_comps_append["weapon_" + str(j)] = list(f2p_comps_dict[comp][i]["weapon"])[0]
    #                 if len(list(f2p_comps_dict[comp][i]["artifacts"])):
    #                     f2p_comps_append["artifact_" + str(j)] = list(f2p_comps_dict[comp][i]["artifacts"])[0]
    #                 else:
    #                     f2p_comps_append["artifact_" + str(j)] = "-"
    #                 j += 1
    #             f2p_comps.append(f2p_comps_append)

    exc_comps = []
    comp_names = []
    variations = {}
    for comp in comps_dict:
        if comp in skip_comps:
            continue
        if info_char and filename not in comp:
            continue
        comp_name = comps_dict[comp]["comp_name"]
        alt_comp_name = comps_dict[comp]["alt_comp_name"]
        # Only one variation of each comp name is included,
        # unless if it's used for a character's infographic
        if comp_name not in comp_names or comp_name == "-" or info_char:
            if comps_dict[comp]["app_rate"] > app_rate_threshold or (info_char and comps_dict[comp]["app_rate"] > char_app_rate_threshold):
                if comp not in comps_list:
                    add_comp_list = input("Input " + str(comp) + " / " + comp_name + "? (y/n)")
                    if add_comp_list == "y":
                        comps_list_csv_writer.writerow(comp)
                temp_comp_name = "-"
                if alt_comp_name != "-":
                    temp_comp_name = alt_comp_name
                else:
                    temp_comp_name = comp_name
                out_comps_append = {
                    "comp_name": temp_comp_name,
                    "char_1": comp[0],
                    "char_2": comp[1],
                    "char_3": comp[2],
                    "char_4": comp[3],
                    "app_rate": str(comps_dict[comp]["app_rate"]) + "%",
                    "own_rate": str(comps_dict[comp]["own_rate"]) + "%",
                    "usage_rate": str(comps_dict[comp]["usage_rate"]) + "%"
                }
                # out_comps_append["app_flat"] = str(len(comps_dict[comp]["players"]))
                j = 1
                if floor:
                    try:
                        for i in comp:
                            out_comps_append["weapon_" + str(j)] = list(comps_dict[comp][i]["weapon"])[0]
                            if len(list(comps_dict[comp][i]["artifacts"])):
                                out_comps_append["artifact_" + str(j)] = list(comps_dict[comp][i]["artifacts"])[0]
                            else:
                                out_comps_append["artifact_" + str(j)] = "-"
                            j += 1
                    except Exception as e:
                        print(comp)
                        print(comps_dict[comp])
                        print(i)
                        print(j)
                        print('{}, {}'.format(e, type(e)))
                if info_char:
                    if comp_name not in comp_names:
                        variations[comp_name] = 1
                        out_comps_append["variation"] = variations[comp_name]
                        out_comps.append(out_comps_append)
                    else:
                        variations[comp_name] += 1
                        out_comps_append["variation"] = variations[comp_name]
                        var_comps.append(out_comps_append)
                else:
                    out_comps.append(out_comps_append)
                comp_names.append(comp_name)
            elif floor:
                temp_comp_name = "-"
                if alt_comp_name != "-":
                    temp_comp_name = alt_comp_name
                else:
                    temp_comp_name = comp_name
                exc_comps_append = {
                    "comp_name": temp_comp_name,
                    "char_1": comp[0],
                    "char_2": comp[1],
                    "char_3": comp[2],
                    "char_4": comp[3],
                    "app_rate": str(comps_dict[comp]["app_rate"]) + "%",
                    "own_rate": str(comps_dict[comp]["own_rate"]) + "%",
                    "usage_rate": str(comps_dict[comp]["usage_rate"]) + "%",
                }
                exc_comps.append(exc_comps_append)
        elif comp_name in comp_names:
            temp_comp_name = "-"
            if alt_comp_name != "-":
                temp_comp_name = alt_comp_name
            else:
                temp_comp_name = comp_name
            outvar_comps_append = {
                "comp_name": temp_comp_name,
                "char_1": comp[0],
                "char_2": comp[1],
                "char_3": comp[2],
                "char_4": comp[3],
                "app_rate": str(comps_dict[comp]["app_rate"]) + "%",
                "own_rate": str(comps_dict[comp]["own_rate"]) + "%",
                "usage_rate": str(comps_dict[comp]["usage_rate"]) + "%"
            }
            outvar_comps.append(outvar_comps_append)
        if not info_char:
            out = name_filter(comp, mode="out")
            for i in range(len(out)):
                if out[i] == "Yun Jin":
                    out[i] = "Yunjin"
                    break
            out_json.append({
                "char_one": out[0],
                "char_two": out[1],
                "char_three": out[2],
                "char_four": out[3],
                "usage_rate": comps_dict[comp]["usage_rate"],
                "rank": comps_dict[comp]["usage_rank"]
            })

    if info_char:
        out_comps += var_comps

    if archetype != "all":
        filename = filename + "_" + archetype

    if whaleCheck:
        if not(whaleCheckOnly):
            filename = filename + "_C0"
        else:
            filename = filename + "_C1"

    if floor and not info_char:
        pass
        # csv_writer = csv.writer(open("../comp_results/f2p_app_" + filename + ".csv", 'w', newline=''))
        # for comps in f2p_comps:
        #     csv_writer.writerow(comps.values())
        # with open("../comp_results/var_" + filename + ".json", "w") as out_file:
        #     out_file.write(json.dumps(outvar_comps,indent=4))

    if floor:
        csv_writer = csv.writer(open("../comp_results/comps_usage_" + filename + ".csv", 'w', newline=''))
        for comps in out_comps:
            csv_writer.writerow(comps.values())
        # with open("../comp_results/exc_" + filename + ".json", "w") as out_file:
        #     out_file.write(json.dumps(exc_comps,indent=4))

    if not info_char:
        with open("../comp_results/json/" + filename + ".json", "w") as out_file:
            out_file.write(json.dumps(out_json,indent=4))

def duo_write(duos_dict, usage, filename):
    out_duos = []
    temp_out_duos = []
    for char in duos_dict:
        if usage[RECENT_PHASE][char]["app"] > 1:
            out_duos_append = {
                "char": char,
                # "duration": usage[RECENT_PHASE][char]["duration"],
                "app": usage[RECENT_PHASE][char]["app"],
                "usage": usage[RECENT_PHASE][char]["usage"],
            }
            for i in range(8):
                if i < len(duos_dict[char]):
                    out_duos_append["app_rate_" + str(i + 1)] = str(duos_dict[char][i][1]) + "%"
                    out_duos_append["char_" + str(i + 1)] = duos_dict[char][i][0]
                else:
                    out_duos_append["app_rate_" + str(i + 1)] = "0%"
                    out_duos_append["char_" + str(i + 1)] = "-"
            out_duos.append(out_duos_append)
    out_duos = sorted(out_duos, key=lambda t: t["usage"], reverse = True)

    for char in out_duos:
        del char["app"]
    #     if char["app"] > 5:
    #         temp_out_duos.append(char.copy())
    # for char in out_duos:
    #     if char["app"] <= 5:
    #         temp_out_duos.append(char.copy())
    # out_duos = temp_out_duos.copy()

    if archetype != "all":
        filename = filename + "_" + archetype
    csv_writer = csv.writer(open("../char_results/" + filename + ".csv", 'w', newline=''))
    for duos in out_duos:
        csv_writer.writerow(duos.values())

def char_usages_write(chars_dict, filename, floor):
    out_chars = []
    temp_chars_dict = {}
    weap_len = 8
    arti_len = 6
    chars_dict = dict(sorted(chars_dict.items(), key=lambda t: t[1]["usage"], reverse=True))

    # for char in chars_dict:
    #     if chars_dict[char]["app"] > 5:
    #         temp_chars_dict[char] = chars_dict[char].copy()
    # for char in chars_dict:
    #     if chars_dict[char]["app"] <= 5:
    #         temp_chars_dict[char] = chars_dict[char].copy()
    # chars_dict = temp_chars_dict.copy()

    for char in chars_dict:
        if floor:
            if "12 build" == filename:
                weap_len = 8
                arti_len = 6
            out_chars_append = {
                "char": char,
                "usage_rate": str(chars_dict[char]["usage"]) + "%",
                "app_rate": str(chars_dict[char]["app"]) + "%",
                "own_rate": str(chars_dict[char]["own"]) + "%",
                "duration_1": chars_dict[char]["duration_1"],
                "duration_2": chars_dict[char]["duration_2"],
                "role": chars_dict[char]["role"],
                "rarity": chars_dict[char]["rarity"],
                "diff": str(chars_dict[char]["diff"]) + "%"
            }
            for i in ["app_rate","own_rate","usage_rate","diff"]:
                if out_chars_append[i] == "-%":
                    out_chars_append[i] = "-"
            for i in range(weap_len):
                out_chars_append["weapon_" + str(i + 1)] = list(chars_dict[char]["weapons"])[i]
                out_chars_append["weapon_" + str(i + 1) + "_app"] = str(list(chars_dict[char]["weapons"].values())[i]) + "%"
                if out_chars_append["weapon_" + str(i + 1) + "_app"] == "-%":
                    out_chars_append["weapon_" + str(i + 1) + "_app"] = "-"
            for i in range(arti_len):
                out_chars_append["artifact_" + str(i + 1)] = list(chars_dict[char]["artifacts"])[i]
                out_chars_append["artifact_" + str(i + 1) + "_app"] = str(list(chars_dict[char]["artifacts"].values())[i]) + "%"
                if out_chars_append["artifact_" + str(i + 1) + "_app"] == "-%":
                    out_chars_append["artifact_" + str(i + 1) + "_app"] = "-"
            for i in range(7):
                out_chars_append["use_" + str(i)] = str(list(list(chars_dict[char]["cons_usage"].values())[i].values())[2]) + "%"
                if out_chars_append["use_" + str(i)] == "-%":
                    out_chars_append["use_" + str(i)] = "-"
            for i in range(7):
                out_chars_append["own_" + str(i)] = str(list(list(chars_dict[char]["cons_usage"].values())[i].values())[1]) + "%"
                if out_chars_append["own_" + str(i)] == "-%":
                    out_chars_append["own_" + str(i)] = "-"
            for i in range(7):
                out_chars_append["app_" + str(i)] = str(list(list(chars_dict[char]["cons_usage"].values())[i].values())[0]) + "%"
                if out_chars_append["app_" + str(i)] == "-%":
                    out_chars_append["app_" + str(i)] = "-"
            out_chars_append["cons_avg"] = chars_dict[char]["cons_avg"]
            out_chars_append["sample"] = chars_dict[char]["sample"]
            out_chars.append(out_chars_append)
            if char == filename:
                break
        else:
            out_chars_append = {
                "char": char,
                "usage_rate": str(chars_dict[char]["usage"]) + "%",
                "app_rate": str(chars_dict[char]["app"]) + "%",
                "own_rate": str(chars_dict[char]["own"]) + "%",
                "duration_1": chars_dict[char]["duration_1"],
                "duration_2": chars_dict[char]["duration_2"],
                "role": chars_dict[char]["role"],
                "rarity": chars_dict[char]["rarity"],
                "diff": str(chars_dict[char]["diff"]) + "%",
            }
            for i in ["app_rate","own_rate","usage_rate","diff"]:
                if out_chars_append[i] == "-%":
                    out_chars_append[i] = "-"
            out_chars.append(out_chars_append)

    if archetype != "all":
        filename = filename + "_" + archetype
    csv_writer = csv.writer(open("../char_results/" + filename + ".csv", 'w', newline=''))
    count = 0
    for chars in out_chars:
        if count == 0:
            header = chars.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(chars.values())
    with open("../char_results/" + filename + ".json", "w") as out_file:
        out_file.write(json.dumps(out_chars,indent=2))

def name_filter(comp, mode="out"):
    filtered = []
    if mode == "out":
        for char in comp:
            if CHARACTERS[char]["out_name"]:
                filtered.append(CHARACTERS[char]["alt_name"])
            else:
                filtered.append(char)
    return filtered
    #TODO Need to create a structure for bad names --> names 

def comp_chars(row):
    comp = []
    for i in range(4, 8):
        if row[i] != "":
            comp.append(row[i])
    return comp

def form_comps(col_names, table, info_char):
    room = col_names.index('half')
    comps = []
    comp_len = {"1": 0, "2": 0, "3": 0, "4": 0}
    duration_array = {"12": {
        "1": [],
        "2": [],
    }, "11": {
        "1": [],
        "2": [],
    }}
    lenient = {"12": {
        "1": 200,
        "2": 200,
    }, "11": {
        "1": 200,
        "2": 200,
    }}
    strict = {"12": {
        "1": 200,
        "2": 200,
    }, "11": {
        "1": 200,
        "2": 200,
    }}

    for i in range(len(table)):
        if "3-2" != table[i][room][-3:]:
            date_format = "%Y-%m-%d %H:%M:%S"
            date_start = datetime.strptime(table[i][8].split("+")[0], date_format)
            date_end = datetime.strptime(table[i + 1][8].split("+")[0], date_format)
            duration = int((date_end - date_start).seconds)
            # if duration > 200 or duration == 0:
            #     duration = None
            if (duration > lenient[str(table[i][room][:2])][str(table[i][room][-1:])] or duration <= 0):
                duration = None
            else:
                duration_array[str(table[i][room][:2])][str(table[i][room][-1:])].append(duration)
                if duration > strict[str(table[i][room][:2])][str(table[i][room][-1:])]:
                    duration = None
        else:
            duration = None
        # comp_temp = comp_chars(table[i])
        # if table[i][room][:2] == "12":
        #     comp_len[str(len(comp_temp))] += 1
        comp = Composition(table[i][0], comp_chars(table[i]), RECENT_PHASE, table[i][room], duration, info_char)
        comps.append(comp)

    # print(comp_len)

    # for floor_iter in ["11", "12"]:
    #     for side_iter in ["1", "2"]:
    #         plt.hist(duration_array[floor_iter][side_iter])
    #         plt.title(floor_iter + ' Side ' +  side_iter)
    #         plt.savefig('../comp_results/' + floor_iter + ' Side ' +  side_iter + '.png')
    #         plt.close()
    # exit()

    return comps

def add_players_comps(players, comps):
    for comp in comps:
        if comp.phase in players:
            if comp.player in players[comp.phase]:
                players[comp.phase][comp.player].add_comp(comp)

def form_players(table, comps, phases):
    # index 0 is player id, 1 is phase, 2 is character name, 3 is character level
    # 4 is constellation, 5 is weapons, 6 is artifacts
    players = {}
    for phase in phases:
        players[phase] = {}

    phase = table[0][1]
    id = table[0][0]
    player = PlayerPhase(id, phase)
    for row in table:
        if row[0] != id or row[1] != phase:
            players[phase][id] = player
            id = row[0]
            phase = row[1]
            player = PlayerPhase(id, phase)
        player.add_character(row[2], row[3], row[4], row[5], row[6], row[7])
    players[phase][id] = player

    add_players_comps(players, comps)
    return players

main()
