import json

# Set class constants in initialization
# Load the list of characters from their file
with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

# Load the list of elements from the reactions file
with open('../data/reaction.json') as react_file:
    ELEMENTS = list(json.load(react_file).keys())

class Composition:
    """An object that stores information about a particular composition. Has:
        player: a string for the player who used this comp.
        phase: a string for the phase this composition was used in.
        room: a string in the form XX-X-X for the room this comp was used in.
        char_presence: a string --> boolean dict for chars in this comp.
        characters: a list of strings for the names of the chars in this comp.
        elements: a string --> int dict for the num of chars for each element.
        resonance: a string --> boolean dict for which resonances are active.
        
        Additional methods are:
        resonance_string: returns the resonances active as a string.
        on_res_chars: returns the list of characters activating the resonance.
        char_elemeent_list: returns the list of character's elements.
    """

    def __init__(self, uid, comp_chars, phase, room):
        """Composition constructor. Takes in:
            A player, as a UID string
            A composition, as a length-four list of character strings
            A phase, as a string
            A room, as a string
        """
        self.player = str(uid)
        self.phase = phase
        self.room = room
        self.char_structs(comp_chars)
        self.name_structs(self.characters)
        self.comp_elements()

    def char_structs(self, comp_chars):
        """Character structure creator.
        Makes a presence dict that maps character names to bools, and
        a list (alphabetically ordered) of the character names.
        """
        self.char_presence = {}
        fives = []
        dps = []
        sub = []
        anemo = []
        healer = []
        temp = []
        temp_remove = []
        for character in CHARACTERS.keys():
            self.char_presence[character] = character in comp_chars
            if self.char_presence[character]:
                if CHARACTERS[character]["availability"] in ["Limited 5*", "5*"]:
                    fives.append(character)

                if character in ["Tartaglia","Kamisato Ayaka","Hu Tao","Xiao","Eula","Arataki Itto","Razor","Diluc","Yoimiya","Keqing","Noelle","Klee"]:
                    dps.insert(0, character)
                elif character in ["Bennett","Qiqi","Diona","Sayu"]:
                    healer.append(character)
                elif character in ["Kaedehara Kazuha","Venti","Traveler-A"]:
                    anemo.append(character)
                elif character in ["Thoma"]:
                    healer.insert(0, character)
                elif character in ["Raiden Shogun"]:
                    dps.append(character)
                elif character in ["Shenhe","Gorou","Mona","Kujou Sara","Rosaria","Fischl","Kaeya","Yun Jin","Lisa","Traveler-G","Aloy","Traveler-E","Xinyan"]:
                    sub.insert(0, character)
                elif character in ["Beidou","Chongyun","Amber"]:
                    sub.append(character)
                else:
                    temp.append(character)
        for character in temp:
            if character in ["Xingqiu", "Yelan"]:
                # If Childe is DPS, Xingqiu is ahead of Xiangling
                if "Tartaglia" in dps:
                    dps.insert(1, character)
                    temp_remove.append(character)
                    continue
                else:
                    sub.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Zhongli"]:
                # For Xiao Succ Benny Dong
                if (
                    "Sucrose" in temp or
                    "Kaedehara Kazuha" in anemo or
                    "Venti" in anemo
                ) and "Bennett" in healer and "Xiao" in dps:
                    healer.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    healer.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Albedo"]:
                if "Zhongli" in temp:
                    anemo.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    sub.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Yae Miko"]:
                if "Raiden Shogun" in dps:
                    dps.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    sub.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Barbara"]:
                if healer:
                    sub.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    healer.append(character)
                    temp_remove.append(character)
                    continue

            if dps:
                if character in ["Ningguang","Ganyu","Kamisato Ayato"]:
                    sub.insert(0, character)
                    temp_remove.append(character)
                    continue
                elif character in ["Yanfei"]:
                    healer.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Ningguang","Yanfei","Ganyu","Kamisato Ayato"]:
                dps.append(character)
                temp_remove.append(character)
                continue
        for character in temp_remove:
            temp.remove(character)
        temp_remove = []
        for character in temp:
            if character in ["Xiangling"]:
                if "Kamisato Ayato" in sub:
                    sub.insert(1, character)
                    temp_remove.append(character)
                    continue
                else:
                    sub.insert(0, character)
                    temp_remove.append(character)
                    continue

            if "Xiao" in dps:
                if character in ["Jean","Sucrose"]:
                    dps.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Jean"]:
                anemo.insert(0, character)
                temp_remove.append(character)
                continue

            if dps:
                if character in ["Sucrose"]:
                    # For Sukokomon, where Kokomi is DPS and Xiangling, Fischl is sub
                    if "Fischl" in sub and "Xiangling" in temp:
                        dps.append(character)
                        temp_remove.append(character)
                        continue
                    else:
                        anemo.append(character)
                        temp_remove.append(character)
                        continue
                if healer and "Zhongli" not in healer:
                    if character in ["Sangonomiya Kokomi"]:
                        sub.append(character)
                        temp_remove.append(character)
                        continue
                else:
                    if character in ["Sangonomiya Kokomi"]:
                        sub.append(character)
                        temp_remove.append(character)
                        continue
            else:
                if character in ["Sangonomiya Kokomi"]:
                    dps.insert(0, character)
                    temp_remove.append(character)
                    continue

        for character in temp_remove:
            temp.remove(character)
        for character in temp:
            if character in ["Sucrose"]:
                if "Xiangling" in sub:
                    anemo.insert(0, character)
                    temp_remove.append(character)
                    continue
                else:
                    dps.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Traveler"]:
                sub.insert(0, character)
                temp_remove.append(character)
                continue
            else:
                # print("dps: " + str(dps) + ", sub: " + str(sub) + ", anemo: " + str(anemo) + ", healer: " + str(healer))
                print("not included: " + str(temp))
        self.fivecount = len(fives)
        self.characters = dps + sub + anemo + healer

    def name_structs(self, characters):
        """Name structure creator.
        """
        comp_names = {
            "Morgana": [
            # Ganyu and Diona/Zhongli, no Shenhe/Rosaria/Ayaka
                ["Ganyu","Mona","Venti","Diona"],
                ["Ganyu","Mona","Kaedehara Kazuha","Diona"],
                ["Ganyu","Mona","Sucrose","Diona"],
                ["Ganyu","Mona","Venti","Zhongli"],
                ["Ganyu","Kamisato Ayato","Venti","Diona"],
                ["Ganyu","Kamisato Ayato","Kaedehara Kazuha","Diona"]
            ],
            "Moryana": [
            # Ayaka and Diona/Zhongli, no Shenhe/Rosaria/Ganyu
                ["Kamisato Ayaka","Mona","Venti","Diona"],
                ["Kamisato Ayaka","Mona","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Mona","Sucrose","Diona"],
                ["Kamisato Ayaka","Mona","Zhongli","Diona"],
                ["Kamisato Ayaka","Mona","Venti","Zhongli"],
                ["Kamisato Ayaka","Xingqiu","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Xingqiu","Venti","Diona"],
                ["Kamisato Ayaka","Xingqiu","Sucrose","Diona"],
                ["Kamisato Ayaka","Yelan","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Yelan","Venti","Diona"],
                ["Kamisato Ayaka","Yelan","Sucrose","Diona"],
                ["Kamisato Ayaka","Sangonomiya Kokomi","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Sangonomiya Kokomi","Venti","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Venti","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Sucrose","Diona"]
            ],
            "Freeze Ayaka/Ganyu": [
            # Ayaka and Ganyu, no Rosaria/Shenhe
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Mona","Venti"],
                ["Kamisato Ayaka","Ganyu","Mona","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Mona","Zhongli"]
            ],
            "Freeze Ganyu": [
            # Ganyu and Rosaria/Shenhe, no Ayaka
                ["Ganyu","Shenhe","Mona","Venti"],
                ["Ganyu","Shenhe","Sangonomiya Kokomi","Venti"],
                ["Ganyu","Rosaria","Mona","Venti"],
                ["Ganyu","Rosaria","Mona","Zhongli"],
                ["Ganyu","Rosaria","Sangonomiya Kokomi","Venti"],
                ["Ganyu","Rosaria","Kaedehara Kazuha","Zhongli"]
            ],
            "Freeze Ayaka": [
            # Ayaka and Rosaria/Shenhe, no Ayaka
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Mona","Venti"],
                ["Kamisato Ayaka","Shenhe","Mona","Sucrose"],
                ["Kamisato Ayaka","Shenhe","Mona","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Rosaria","Mona","Venti"],
                ["Kamisato Ayaka","Xingqiu","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Xingqiu","Rosaria","Zhongli"],
                ["Kamisato Ayaka","Yelan","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Yelan","Rosaria","Zhongli"]
            ],
            "Triple Cryo": [
            # 3 cryo, no anemo
                ["Kamisato Ayaka","Shenhe","Mona","Diona"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Diona"],
                ["Kamisato Ayaka","Rosaria","Mona","Diona"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Sangonomiya Kokomi"],
                ["Ganyu","Shenhe","Mona","Diona"]
            ],
            "Mono Cryo": [["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Diona"]],
            # 3 cryo, anemo
            "Tapu Koko": [
            # Kokomi, electro
                ["Sangonomiya Kokomi","Yae Miko","Fischl","Sucrose"],
                ["Sangonomiya Kokomi","Fischl","Beidou","Sucrose"],
                ["Sangonomiya Kokomi","Fischl","Beidou","Venti"]
            ],
            "Taser": [
                ["Sucrose","Xingqiu","Fischl","Beidou"],
                ["Sucrose","Yelan","Fischl","Beidou"],
                ["Sucrose","Fischl","Beidou","Barbara"],
                ["Xingqiu","Fischl","Beidou","Kaedehara Kazuha"]
            ],
            "Raiden National Team": [
                ["Raiden Shogun","Xiangling","Xingqiu","Bennett"],
                ["Raiden Shogun","Xiangling","Mona","Bennett"],
                ["Xiangling","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Xingqiu","Sucrose","Bennett"],
                ["Xiangling","Xingqiu","Rosaria","Bennett"],
                ["Xiangling","Xingqiu","Chongyun","Bennett"],
                ["Xiangling","Xingqiu","Venti","Bennett"],
                ["Raiden Shogun","Xiangling","Yelan","Bennett"],
                ["Xiangling","Yelan","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Yelan","Sucrose","Bennett"],
                ["Xiangling","Yelan","Rosaria","Bennett"],
                ["Xiangling","Yelan","Chongyun","Bennett"],
                ["Xiangling","Yelan","Venti","Bennett"]
            ],
            "Raiden Soup": [
            # Raiden, hydro, anemo, pyro
                ["Raiden Shogun","Xingqiu","Venti","Bennett"],
                ["Raiden Shogun","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Xingqiu","Sucrose","Bennett"],
                ["Raiden Shogun","Xiangling","Xingqiu","Sucrose"],
                ["Raiden Shogun","Yelan","Venti","Bennett"],
                ["Raiden Shogun","Yelan","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Yelan","Sucrose","Bennett"],
                ["Raiden Shogun","Xiangling","Yelan","Sucrose"],
                ["Raiden Shogun","Mona","Venti","Bennett"]
            ],
            "Raiden Hypercarry": [
            # Raiden, Sara, anemo, Bennett
                ["Raiden Shogun","Kujou Sara","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Kujou Sara","Sucrose","Bennett"],
                ["Raiden Shogun","Kujou Sara","Venti","Bennett"]
            ],
            "Raikou": [
            # Raiden, Yae, anemo, Bennett
                ["Raiden Shogun","Yae Miko","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Yae Miko","Sucrose","Bennett"],
                ["Raiden Shogun","Yae Miko","Venti","Bennett"]
            ],
            "Raiden Taser": [
            # Raiden, hydro, no other suitable comps
                ["Raiden Shogun","Yae Miko","Sangonomiya Kokomi","Sucrose"],
                ["Raiden Shogun","Yae Miko","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Sucrose"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Venti"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Bennett"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Sangonomiya Kokomi"],
                ["Raiden Shogun","Xingqiu","Fischl","Sucrose"],
                ["Raiden Shogun","Xingqiu","Fischl","Bennett"],
                ["Raiden Shogun","Xingqiu","Kujou Sara","Bennett"],
                ["Raiden Shogun","Xingqiu","Sucrose","Barbara"],
                ["Raiden Shogun","Xingqiu","Venti","Zhongli"],
                ["Raiden Shogun","Yae Miko","Yelan","Sucrose"],
                ["Raiden Shogun","Yae Miko","Yelan","Venti"],
                ["Raiden Shogun","Yae Miko","Yelan","Bennett"],
                ["Raiden Shogun","Yae Miko","Yelan","Sangonomiya Kokomi"],
                ["Raiden Shogun","Yelan","Fischl","Sucrose"],
                ["Raiden Shogun","Yelan","Fischl","Bennett"],
                ["Raiden Shogun","Yelan","Kujou Sara","Bennett"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Venti","Zhongli"]
            ],
            "Double Hydro Raiden": [
            # Raiden, 2 hydro
                ["Raiden Shogun","Xingqiu","Mona","Bennett"],
                ["Raiden Shogun","Xingqiu","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Xingqiu","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Xingqiu","Venti","Barbara"],
                ["Raiden Shogun","Xingqiu","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Mona","Bennett"],
                ["Raiden Shogun","Yelan","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Yelan","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Yelan","Venti","Barbara"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"]
            ],
            "Overvape Raiden/Ayato": [["Raiden Shogun","Kamisato Ayato","Xiangling","Bennett"]],
            "PosEidon": [
            # Raiden, Ayato, anemo, Bennett
                ["Raiden Shogun","Kamisato Ayato","Venti","Bennett"],
                ["Raiden Shogun","Kamisato Ayato","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Kamisato Ayato","Sucrose","Bennett"]
            ],
            "Overload Raiden": [
            # Raiden, Xiangling, Bennett, no hydro
                ["Raiden Shogun","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Xiangling","Venti","Bennett"],
                ["Raiden Shogun","Xiangling","Sucrose","Bennett"],
                ["Raiden Shogun","Yae Miko","Xiangling","Bennett"],
                ["Raiden Shogun","Xiangling","Fischl","Bennett"],
                ["Raiden Shogun","Xiangling","Kujou Sara","Bennett"],
                ["Raiden Shogun","Xiangling","Zhongli","Bennett"]
            ],
            "Mono Electro": [["Raiden Shogun","Yae Miko","Jean","Venti"]],
            # electro and anemo only
            "Double Geo Xiao": [
                ["Xiao","Jean","Albedo","Zhongli"],
                ["Xiao","Jean","Traveler-G","Zhongli"],
                ["Xiao","Sucrose","Albedo","Zhongli"],
                ["Xiao","Venti","Albedo","Zhongli"],
                ["Xiao","Albedo","Zhongli","Bennett"]
            ],
            "Xiao Succ Benny Dong": [
                ["Xiao","Sucrose","Bennett","Zhongli"],
                ["Xiao","Venti","Bennett","Zhongli"],
                ["Xiao","Jean","Zhongli","Bennett"]
            ],
            "Double Pyro Xiao": [
                ["Xiao","Sucrose","Xiangling","Bennett"],
                ["Xiao","Xiangling","Zhongli","Bennett"]
            ],
            "Mono Geo Itto": [["Arataki Itto","Gorou","Albedo","Zhongli"]],
            "Triple Geo Itto": [
                ["Arataki Itto","Gorou","Zhongli","Bennett"],
                ["Arataki Itto","Gorou","Albedo","Bennett"],
                ["Arataki Itto","Albedo","Zhongli","Bennett"]
            ],
            "Mono Geo Noelle": [
                ["Noelle","Gorou","Albedo","Zhongli"],
                ["Noelle","Yun Jin","Gorou","Albedo"]
            ],
            "Double Geo Hu Tao": [
                ["Hu Tao","Xingqiu","Albedo","Zhongli"],
                ["Hu Tao","Xingqiu","Ningguang","Zhongli"],
                ["Hu Tao","Xingqiu","Traveler-G","Zhongli"],
                ["Hu Tao","Yelan","Albedo","Zhongli"],
                ["Hu Tao","Yelan","Ningguang","Zhongli"]
            ],
            "Double Hydro Hu Tao": [
                ["Hu Tao","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Xingqiu","Sucrose"],
                ["Hu Tao","Yelan","Xingqiu","Zhongli"]
            ],
            "Double Pyro Hu Tao": [["Hu Tao","Xiangling","Xingqiu","Zhongli"]],
            "VapeMelt Hu Tao": [
                ["Hu Tao","Xingqiu","Ganyu","Zhongli"],
                ["Hu Tao","Xingqiu","Chongyun","Zhongli"],
                ["Hu Tao","Xingqiu","Rosaria","Diona"],
                ["Hu Tao","Xingqiu","Rosaria","Zhongli"],
                ["Hu Tao","Xingqiu","Sucrose","Diona"],
                ["Hu Tao","Yelan","Ganyu","Zhongli"],
                ["Hu Tao","Yelan","Chongyun","Zhongli"],
                ["Hu Tao","Yelan","Rosaria","Diona"],
                ["Hu Tao","Yelan","Rosaria","Zhongli"],
                ["Hu Tao","Yelan","Sucrose","Diona"]
            ],
            "VV Vape Hu Tao": [
            # Hu Tao, Xingqiu, anemo, pyro
                ["Hu Tao","Xingqiu","Sucrose","Bennett"],
                ["Hu Tao","Xingqiu","Sucrose","Thoma"],
                ["Hu Tao","Xingqiu","Sucrose","Yanfei"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Thoma"],
                ["Hu Tao","Yelan","Sucrose","Bennett"],
                ["Hu Tao","Yelan","Sucrose","Thoma"]
            ],
            "Vape Hu Tao": [
            # Hu Tao, Xingqiu, no other suitable comps
                ["Hu Tao","Xingqiu","Sucrose","Zhongli"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Zhongli"],
                ["Hu Tao","Xingqiu","Venti","Zhongli"],
                ["Hu Tao","Xingqiu","Zhongli","Bennett"],
                ["Hu Tao","Xingqiu","Mona","Zhongli"],
                ["Hu Tao","Yelan","Sucrose","Zhongli"],
                ["Hu Tao","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Hu Tao","Yelan","Venti","Zhongli"],
                ["Hu Tao","Yelan","Zhongli","Bennett"],
                ["Hu Tao","Yelan","Mona","Zhongli"]
            ],
            "Overvape Hu Tao": [["Hu Tao","Xingqiu","Fischl","Zhongli"]],
            "Hu Tao/Raiden Dual Carry": [["Hu Tao","Raiden Shogun","Xingqiu","Zhongli"]],
            "Melt Ayaka/Hu Tao": [
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Yelan","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Diona"]
            ],
            "Melt Ayaka": [
                ["Kamisato Ayaka","Xiangling","Shenhe","Bennett"],
                ["Kamisato Ayaka","Xiangling","Rosaria","Bennett"]
            ],
            "Ayato Hypercarry": [
            # Ayato, Yun Jin, anemo, Bennett
                ["Kamisato Ayato","Yun Jin","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Yun Jin","Venti","Bennett"]
            ],
            "Reverse Vape Ayato": [
            # Ayato, Xiangling, Bennett
                ["Kamisato Ayato","Xiangling","Sucrose","Bennett"],
                ["Kamisato Ayato","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Xiangling","Venti","Bennett"],
                ["Kamisato Ayato","Xiangling","Zhongli","Bennett"],
                ["Kamisato Ayato","Xiangling","Yun Jin","Bennett"],
                ["Kamisato Ayato","Xiangling","Xingqiu","Bennett"],
                ["Kamisato Ayato","Xiangling","Yelan","Bennett"]
            ],
            "Double Hydro Ayato": [
            # 2 hydro, anemo, Bennett
                ["Kamisato Ayato","Xingqiu","Venti","Bennett"],
                ["Kamisato Ayato","Xingqiu","Sucrose","Bennett"],
                ["Kamisato Ayato","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Yelan","Venti","Bennett"],
                ["Kamisato Ayato","Yelan","Sucrose","Bennett"],
                ["Kamisato Ayato","Yelan","Kaedehara Kazuha","Bennett"]
            ],
            "Ayato Soup": [["Kamisato Ayato","Fischl","Kaedehara Kazuha","Bennett"]],
            # Ayato, electro, anemo, pyro
            "Ayato Taser": [["Kamisato Ayato","Fischl","Beidou","Sucrose"]],
            # Ayato, electro, anemo, no pyro
            "International Childe": [
            # Childe, Xiangling, flex, Bennett
                ["Tartaglia","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Tartaglia","Xiangling","Sucrose","Bennett"],
                ["Tartaglia","Xiangling","Venti","Bennett"],
                ["Tartaglia","Xiangling","Zhongli","Bennett"]
            ],
            "Double Hydro Childe": [
            # Childe, Xingqiu, anemo, Bennett
                ["Tartaglia","Xingqiu","Venti","Bennett"],
                ["Tartaglia","Xingqiu","Sucrose","Bennett"],
                ["Tartaglia","Xingqiu","Xiangling","Bennett"],
                ["Tartaglia","Yelan","Venti","Bennett"],
                ["Tartaglia","Yelan","Sucrose","Bennett"],
                ["Tartaglia","Yelan","Xiangling","Bennett"]
            ],
            "Fireworks": [["Tartaglia","Fischl","Beidou","Bennett"]],
            "Childe/Raiden Dual Carry": [["Tartaglia","Raiden Shogun","Xiangling","Bennett"]],
            "Melt Ganyu": [
                ["Ganyu","Xiangling","Zhongli","Bennett"],
                ["Ganyu","Xiangling","Venti","Bennett"],
                ["Ganyu","Xiangling","Bennett","Diona"]
            ],
            "Eula/Raiden/Zhongli/Bennett": [["Eula","Raiden Shogun","Zhongli","Bennett"]],
            "Eula/Raiden/Venti/Bennett": [["Eula","Raiden Shogun","Venti","Bennett"]],
            "Eula/Raiden Shogun/Venti/Diona": [["Eula","Raiden Shogun","Venti","Diona"]],
            "Eula/Rosaria/Jean/Zhongli": [["Eula","Rosaria","Jean","Zhongli"]],
            "Triple Polearm Eula": [["Eula","Raiden Shogun","Rosaria","Zhongli"]],
            "Double Electo Eula": [["Eula","Fischl","Beidou","Diona"]],
            "Triple Cryo Eula": [["Eula","Rosaria","Fischl","Diona"]],
            "Vape Yoimiya": [
                ["Yoimiya","Yelan","Yun Jin","Zhongli"],
                ["Yoimiya","Xingqiu","Zhongli","Bennett"],
                ["Yoimiya","Xingqiu","Yun Jin","Bennett"]
            ],
            "Overvape Yoimiya": [
                ["Yoimiya","Xingqiu","Fischl","Zhongli"],
                ["Yoimiya","Xingqiu","Fischl","Bennett"]
            ],
            "Vape Diluc": [
                ["Diluc","Xingqiu","Zhongli","Bennett"],
                ["Diluc","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Diluc","Xingqiu","Sucrose","Bennett"]
            ],
            "Vape Yanfei": [["Yanfei","Xingqiu","Sucrose","Bennett"]],
            "Double Geo Diluc": [["Diluc","Xingqiu","Albedo","Zhongli"]],
            "Quickswap Keqing": [["Keqing","Xingqiu","Sucrose","Bennett"]],
            "Sukokomon": [["Sangonomiya Kokomi","Sucrose","Xiangling","Fischl"]],
            "Reverse Melt Quickswap": [
                ["Xiangling","Rosaria","Kaeya","Bennett"],
                ["Xiangling","Rosaria","Chongyun","Bennett"]
            ],
            "Double Geo Double Pyro": [["Ningguang","Xiangling","Zhongli","Bennett"]],
            "Double Pyro Double Hydro": [["Xiangling","Yelan","Xingqiu","Bennett"]]
        }
        self.comp_name = "-"
        for comp_name in comp_names:
            if characters in comp_names[comp_name]:
                self.comp_name = comp_name
                break

    def comp_elements(self):
        """Composition elements tracker.
        Creates a dict that maps elements to number of chars with that element,
        and a dict that maps the resonance(s) the comp has to booleans.
        """
        self.elements = dict.fromkeys(ELEMENTS, 0)
        for char in self.characters:
            self.elements[CHARACTERS[char]["element"]] += 1
        
        self.resonance = dict.fromkeys(ELEMENTS, False)

        # Add the unique resonance to the list of element resonances,
        # and set it as the default. Technically there's the edge case for
        # if there's < 4 characters, it should be false I think?
        self.resonance['Unique'] = len(self.characters) == 4
        for ele in ELEMENTS:
            if self.elements[ele] >= 2:
                self.resonance[ele] = True
                self.resonance['Unique'] = False
    
    def resonance_string(self):
        """Returns the resonance of the composition. Two resos are joined by a ,"""
        resos = []
        for reso in self.resonance.keys():
            if self.resonance[reso]:
                resos.append(reso)
        return ", ".join(resos)
    
    def on_res_chars(self):
        """Returns the list of characters who match the composition's resonance."""
        chars = []
        for char in self.characters:
            if self.resonance[CHARACTERS[char]["element"]] or self.resonance["Unique"]:
                chars.append(char)
        return chars

    def char_element_list(self):
        """Returns the characters' elements as a list"""
        return [ CHARACTERS[char]['element'] for char in self.characters ]

    def contains_chars(self, chars):
        """Returns a bool whether this comp contains all the chars in included list."""
        for char in chars:
            if not self.char_presence[char]:
                return False
        return True
