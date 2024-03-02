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

    def __init__(self, uid, comp_chars, phase, room, duration, info_char):
        """Composition constructor. Takes in:
            A player, as a UID string
            A composition, as a length-four list of character strings
            A phase, as a string
            A room, as a string
        """
        self.player = str(uid)
        self.phase = phase
        self.room = room
        self.duration = duration
        self.char_structs(comp_chars)
        self.name_structs(self.characters, info_char, self.len_element, self.quick_apply, self.slow_apply, self.dps, self.sub, self.anemo, self.healer)
        self.comp_elements()

    def char_structs(self, comp_chars):
        """Character structure creator.
        Makes a presence dict that maps character names to bools, and
        a list (alphabetically ordered) of the character names.
        """
        self.char_presence = {}
        fives = []
        self.dps = []
        self.sub = []
        self.anemo = []
        self.healer = []
        temp = []
        temp_remove = []
        self.len_element = {
            "Anemo": 0,
            "Cryo": 0,
            "Pyro": 0,
            "Geo": 0,
            "Electro": 0,
            "Hydro": 0,
            "Dendro": 0,
        }
        self.quick_apply = {
            "Anemo": 0,
            "Cryo": 0,
            "Pyro": 0,
            "Geo": 0,
            "Electro": 0,
            "Hydro": 0,
            "Dendro": 0,
        }
        self.slow_apply = {
            "Anemo": 0,
            "Cryo": 0,
            "Pyro": 0,
            "Geo": 0,
            "Electro": 0,
            "Hydro": 0,
            "Dendro": 0,
        }
        comp_chars.sort()
        for character in comp_chars:
            self.char_presence[character] = True
            if CHARACTERS[character]["availability"] in ["Limited 5*", "5*"]:
                fives.append(character)

            if CHARACTERS[character]["element"] == "Anemo":
                self.len_element["Anemo"] += 1
            if CHARACTERS[character]["element"] == "Cryo":
                self.len_element["Cryo"] += 1
            if CHARACTERS[character]["element"] == "Pyro":
                self.len_element["Pyro"] += 1
            if CHARACTERS[character]["element"] == "Geo":
                self.len_element["Geo"] += 1
            if CHARACTERS[character]["element"] == "Electro":
                self.len_element["Electro"] += 1
            if CHARACTERS[character]["element"] == "Hydro":
                self.len_element["Hydro"] += 1
            if CHARACTERS[character]["element"] == "Dendro":
                self.len_element["Dendro"] += 1
            if character in ["Xingqiu", "Yelan"]:
                self.quick_apply["Hydro"] += 1
            if character in ["Sangonomiya Kokomi", "Barbara", "Furina"]:
                self.slow_apply["Hydro"] += 1
            if character in ["Ganyu", "Kamisato Ayaka", "Kaeya", "Rosaria", "Layla", "Chongyun", "Wriothesley", "Charlotte"]:
                self.quick_apply["Cryo"] += 1
            if character in ["Eula", "Diona"]:
                self.slow_apply["Cryo"] += 1
            if character in ["Bennett", "Amber"]:
                self.slow_apply["Pyro"] += 1
            if character in ["Xiangling", "Thoma"]:
                self.quick_apply["Pyro"] += 1
            if character in ["Raiden Shogun", "Kuki Shinobu"]:
                self.quick_apply["Electro"] += 1

            if character in ["Tartaglia","Kamisato Ayaka","Tighnari","Hu Tao","Xiao","Eula","Arataki Itto","Razor","Diluc","Yoimiya","Keqing","Noelle","Klee","Shikanoin Heizou","Cyno","Wanderer","Alhaitham","Dehya","Kaveh","Lyney","Freminet","Neuvillette","Wriothesley","Navia","Gaming"]:
                self.dps.insert(0, character)
            elif character in ["Bennett","Qiqi","Diona","Sayu","Kuki Shinobu","Dori","Layla","Yaoyao","Mika","Baizhu","Kirara","Charlotte"]:
                self.healer.append(character)
            elif character in ["Kaedehara Kazuha","Venti","Traveler-A","Lynette"]:
                self.anemo.append(character)
            elif character in ["Thoma","Xianyun"]:
                self.healer.insert(0, character)
            elif character in ["Raiden Shogun"]:
                self.dps.append(character)
            elif character in ["Shenhe","Collei","Gorou","Mona","Kujou Sara","Rosaria","Fischl","Kaeya","Yun Jin","Traveler-G","Aloy","Traveler-E","Xinyan","Traveler-D","Candace","Nahida","Traveler-H","Chevreuse"]:
                self.sub.insert(0, character)
            elif character in ["Beidou","Chongyun","Amber"]:
                self.sub.append(character)
            else:
                temp.append(character)
        for character in temp:
            if character in ["Xingqiu", "Yelan", "Furina"]:
                # If Childe is DPS, Xingqiu is ahead of Xiangling
                if "Tartaglia" in self.dps:
                    self.dps.insert(1, character)
                    temp_remove.append(character)
                    continue
                else:
                    self.sub.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Zhongli"]:
                # For Xiao Succ Benny Dong
                if (
                    "Sucrose" in temp or
                    "Jean" in temp or
                    "Kaedehara Kazuha" in self.anemo or
                    "Venti" in self.anemo or
                    "Faruzan" in temp
                ) and "Bennett" in self.healer and "Xiao" in self.dps:
                    self.healer.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.healer.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Faruzan"]:
                if "Wanderer" in self.dps or "Xiao" in self.dps:
                    self.dps.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.sub.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Nilou"]:
                if "Nahida" in self.sub or "Kaveh" in self.dps:
                    self.sub.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.dps.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Albedo"]:
                if "Zhongli" in temp:
                    self.anemo.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.sub.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Yae Miko"]:
                if "Raiden Shogun" in self.dps:
                    self.dps.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.sub.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Barbara"]:
                if self.healer:
                    self.sub.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    self.healer.append(character)
                    temp_remove.append(character)
                    continue

            if self.dps:
                if "Dehya" in self.dps and character in ["Ganyu"]:
                    self.dps.insert(0, character)
                    temp_remove.append(character)
                    continue
                elif "Raiden Shogun" in self.dps and character in ["Kamisato Ayato"]:
                    self.dps.insert(0, character)
                    temp_remove.append(character)
                    continue
                elif character in ["Ningguang","Ganyu","Kamisato Ayato"]:
                    self.sub.insert(0, character)
                    temp_remove.append(character)
                    continue
                elif character in ["Yanfei"]:
                    self.healer.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Ningguang","Yanfei","Ganyu","Kamisato Ayato"]:
                self.dps.append(character)
                temp_remove.append(character)
                continue
        if "Nahida" in self.sub:
            if not(self.dps):
                self.sub.remove("Nahida")
                self.dps.append("Nahida")
            elif "Raiden Shogun" in self.dps and ("Yae Miko" in self.dps or len(self.dps) == 1):
                self.sub.remove("Nahida")
                self.dps.insert(0, "Nahida")
                self.dps.remove("Raiden Shogun")
                self.sub.insert(0, "Raiden Shogun")
                if "Kamisato Ayato" in self.sub:
                    self.sub.remove("Kamisato Ayato")
                    self.dps.insert(0, "Kamisato Ayato")
        for character in temp_remove:
            temp.remove(character)
        temp_remove = []
        for character in temp:
            if character in ["Xiangling"]:
                if "Kamisato Ayato" in self.sub:
                    self.sub.insert(1, character)
                    temp_remove.append(character)
                    continue
                else:
                    self.sub.insert(0, character)
                    temp_remove.append(character)
                    continue

            if "Xiao" in self.dps:
                if character in ["Jean","Sucrose"]:
                    self.dps.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Jean"]:
                self.anemo.insert(0, character)
                temp_remove.append(character)
                continue

            if self.dps:
                if character in ["Sucrose"]:
                    # For Sukokomon, where Kokomi is DPS and Xiangling+Fischl is self.sub
                    if "Fischl" in self.sub and "Xiangling" in temp:
                        self.dps.append(character)
                        temp_remove.append(character)
                        continue
                    else:
                        self.anemo.append(character)
                        temp_remove.append(character)
                        continue
                if self.healer and "Zhongli" not in self.healer:
                    if character in ["Sangonomiya Kokomi","Lisa"]:
                        self.sub.append(character)
                        temp_remove.append(character)
                        continue
                else:
                    if character in ["Sangonomiya Kokomi","Lisa"]:
                        self.sub.append(character)
                        temp_remove.append(character)
                        continue
            else:
                if character in ["Sangonomiya Kokomi","Lisa"]:
                    if "Yae Miko" in self.sub:
                        self.sub.append(character)
                        temp_remove.append(character)
                        continue
                    elif "Kaeya" in self.sub:
                        self.sub.remove("Kaeya")
                        self.dps.insert(0, "Kaeya")
                        self.sub.append(character)
                        temp_remove.append(character)
                        continue
                    else:
                        self.dps.insert(0, character)
                        temp_remove.append(character)
                        continue

        for character in temp_remove:
            temp.remove(character)
        for character in temp:
            if character in ["Sucrose"]:
                if "Xiangling" in self.sub or "Yae Miko" in self.sub:
                    self.anemo.insert(0, character)
                    temp_remove.append(character)
                    continue
                else:
                    self.dps.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Traveler"]:
                self.sub.insert(0, character)
                temp_remove.append(character)
                continue
            else:
                print("self.dps: " + str(self.dps) + ", self.sub: " + str(self.sub) + ", self.anemo: " + str(self.anemo) + ", self.healer: " + str(self.healer))
                print("not included: " + str(temp))
        self.fivecount = len(fives)
        self.characters = self.dps + self.sub + self.anemo + self.healer

    def name_structs(self, characters, info_char, len_element, quick_apply, slow_apply, dps, sub, anemo, healer):
        """Name structure creator.
        """
        self.comp_name = "-"
        self.alt_comp_name = "-"
        if len(characters) < 4:
            return
        if len_element["Geo"] == 4:
            self.comp_name = "Mono Geo " + characters[0]
        else:
            for elem in len_element:
                if elem == "Pyro":
                    if (len_element[elem] > 1 and len_element[elem] + len_element["Anemo"] + len_element["Geo"] == 4
                        and CHARACTERS[characters[0]]["element"] == "Pyro" and len_element["Geo"] < 2):
                        self.comp_name = "Mono " + elem + " " + characters[0]
                elif (len_element[elem] > 1 and len_element[elem] + len_element["Anemo"] + len_element["Geo"] - slow_apply["Pyro"] == 4
                    and elem != "Anemo" and elem != "Geo" and CHARACTERS[characters[0]]["element"] == elem):
                    self.comp_name = "Mono " + elem + " " + characters[0]

        if self.comp_name == "-":
            if len_element["Dendro"] > 0:
                if len_element["Electro"] > 0:
                    if len_element["Pyro"] == 0 or (
                        slow_apply["Pyro"] > 0 and slow_apply["Pyro"] - len_element["Pyro"] >= 0):
                        if quick_apply["Cryo"] > 0 and len_element["Hydro"] > 0:
                            self.comp_name = "Hyperfridge " + characters[0]
                        elif slow_apply["Hydro"] > 0 and (slow_apply["Hydro"] - len_element["Hydro"] >= 0):
                            self.comp_name = "Quickbloom " + characters[0]
                            if "Yae Miko" in characters and (
                                "Raiden Shogun" in self.comp_name or "Nahida" in self.comp_name):
                                self.comp_name = "Quickbloom Yae"
                            elif "Sangonomiya Kokomi" in characters and "Raiden Shogun" in self.comp_name:
                                self.alt_comp_name = self.comp_name
                                self.comp_name = self.comp_name.replace("Raiden Shogun", "Kokomi")
                        elif len_element["Hydro"] > 0:
                            if slow_apply["Pyro"] > 0 and "Razor" in characters:
                                self.comp_name = "Thundering Furry"
                            elif len(dps) < 2 or (
                                "Nahida" in dps or "Raiden Shogun" in dps or "Xingqiu" in dps or "Yelan" in dps or "Furina" in dps or "Yae Miko" in dps):
                                if characters[0] in ["Raiden Shogun", "Lisa", "Sucrose", "Xingqiu", "Yelan", "Furina", "Fischl", "Traveler-D"]:
                                    self.comp_name = "Hyperbloom Quickswap"
                                else:
                                    self.comp_name = "Hyperbloom " + characters[0]
                        elif slow_apply["Pyro"] > 0:
                            if characters[0] in ["Xingqiu", "Yelan", "Furina", "Fischl", "Traveler-D"]:
                                self.alt_comp_name = "Overburn Quickswap"
                            else:
                                self.alt_comp_name = "Overburn " + characters[0]
                            self.comp_name = self.alt_comp_name.replace("Overburn", "Burning")
                        elif len(dps) < 2 or (
                            "Nahida" in dps or "Raiden Shogun" in dps or "Xingqiu" in dps or "Yelan" in dps or "Furina" in dps or "Yae Miko" in dps):
                            agg_name = characters[0]
                            if CHARACTERS[agg_name]["element"] == "Dendro":
                                self.comp_name = "Spread " + agg_name
                                if "Traveler-D" == agg_name:
                                    self.comp_name = "Aggravate Quickswap"
                                if ("Traveler-D" == agg_name or "Nahida" == agg_name) and "Yae Miko" in characters:
                                    self.comp_name = "Aggravate Yae"
                            else:
                                self.comp_name = "Aggravate " + agg_name
                                if agg_name in ["Raiden Shogun", "Lisa", "Sucrose", "Xingqiu", "Yelan", "Furina", "Fischl"]:
                                    if "Yae Miko" in characters:
                                        self.comp_name = "Aggravate Yae"
                                    else:
                                        self.comp_name = self.comp_name.replace(agg_name, "Quickswap")
                    elif len_element["Hydro"] > 0:
                        if "Razor" in characters:
                            self.comp_name = "Thundering Furry"
                        elif "Cyno" in characters:
                            self.comp_name = "Chaos Cyno"
                        elif len(dps) < 2 or (
                            "Nahida" in dps or "Raiden Shogun" in dps or "Xingqiu" in dps or "Yelan" in dps or "Furina" in dps or "Yae Miko" in dps):
                            self.comp_name = characters[0] + " Curry"
                            if not(CHARACTERS[characters[0]]["element"] == "Dendro" and slow_apply["Hydro"] > 0
                                and slow_apply["Hydro"] - len_element["Hydro"] >= 0):
                                self.alt_comp_name = "Hyperburgeon " + characters[0]
                    else:
                        self.alt_comp_name = "Overburn " + characters[0]
                        self.comp_name = self.alt_comp_name.replace("Overburn", "Burning")
                elif len_element["Pyro"] == 0 and len_element["Hydro"] > 0:
                    if len_element["Cryo"] == 0 or (len_element["Cryo"] == 1 and quick_apply["Cryo"] == 0):
                        self.comp_name = "Bloom Nilou"
                        if "Nilou" != characters[0]:
                            self.alt_comp_name = "Bloom " + characters[0]
                    else:
                        self.comp_name = characters[0] + " Fridge"
                elif len_element["Hydro"] > 0:
                    if len_element["Cryo"] == 0 or (len_element["Cryo"] == 1 and quick_apply["Cryo"] == 0):
                        if quick_apply["Hydro"] > 0 and "Xiangling" in characters and "Bennett" in characters:
                            self.comp_name = "Raiden National Team"
                            if characters[0] == "Xiangling":
                                self.alt_comp_name = characters[2] + " National Team"
                            else:
                                self.alt_comp_name = characters[0] + " National Team"
                        else:
                            if characters[0] in ["Raiden Shogun", "Lisa", "Sucrose", "Xingqiu", "Yelan", "Furina", "Fischl", "Traveler-D", "Xiangling"]:
                                self.comp_name = "Burgeon Quickswap"
                            else:
                                self.comp_name = "Burgeon " + characters[0]
                    else:
                        self.comp_name = characters[0] + " Oven"
                elif quick_apply["Cryo"] > 0:
                    self.comp_name = "Burnmelt " + characters[0]
                elif quick_apply["Pyro"] > 0 or (anemo and len_element["Pyro"] > 0):
                    self.comp_name = "Burning " + characters[0]
            # No dendro
            elif len_element["Pyro"] - slow_apply["Pyro"] > 0:
                if len_element["Hydro"] > 0:
                    if quick_apply["Hydro"] > 0 and "Xiangling" in characters and "Bennett" in characters:
                        if quick_apply["Hydro"] > 1:
                            self.comp_name = "Double Hydro Double Pyro"
                        else:
                            self.comp_name = "Raiden National Team"
                            if len_element["Pyro"] - slow_apply["Pyro"] - quick_apply["Pyro"] > 0:
                                self.alt_comp_name = "Triple Pyro " + characters[0]
                            elif len_element["Hydro"] - slow_apply["Hydro"] - quick_apply["Hydro"] > 0:
                                self.alt_comp_name = "Reverse Vape " + characters[0]
                            elif characters[0] == "Xiangling":
                                self.alt_comp_name = characters[2] + " National Team"
                            else:
                                self.alt_comp_name = characters[0] + " National Team"
                    elif quick_apply["Cryo"] > 0:
                        if len(dps) > 1:
                            self.comp_name = "VapeMelt " + characters[0] + "/" + characters[1]
                        else:
                            self.comp_name = "VapeMelt " + characters[0]
                    elif len_element["Hydro"] > 1 and len_element["Electro"] == 0:
                        if "Xiangling" in characters and "Xingqiu" in characters and "Yelan" in characters and "Hu Tao" in characters:
                            self.comp_name = "Funerational"
                        elif len_element["Electro"] == 0:
                            if (CHARACTERS[characters[0]]["element"] == "Hydro"
                                or CHARACTERS[characters[0]]["element"] == "Anemo"
                                or CHARACTERS[characters[0]]["element"] == "Geo"):
                                self.comp_name = characters[0] + " Hypercarry"
                            else:
                                self.comp_name = "Double Hydro " + characters[0]
                            self.alt_comp_name = "Double Hydro " + characters[0]
                            if len_element["Hydro"] == 3:
                                self.alt_comp_name = self.alt_comp_name.replace("Double Hydro", "Triple Hydro")
                            if characters[0] in ["Xingqiu", "Yelan", "Furina", "Traveler-D", "Xiangling"]:
                                self.comp_name = self.alt_comp_name.replace(characters[0], "Quickswap")
                                self.alt_comp_name = self.alt_comp_name.replace(characters[0], "Quickswap")
                    # elif len_element["Electro"] > 0 and (len(dps) < 2 or "Raiden Shogun" in dps):
                    elif len_element["Electro"] > 0 and (len(dps) < 2 or "Sangonomiya Kokomi" in dps):
                        if "Sangonomiya Kokomi" in characters and "Sucrose" in characters and "Xiangling" in characters and "Fischl" in characters:
                            self.alt_comp_name = "Sukokomon"
                        elif len_element["Anemo"] > 0 and len_element["Pyro"] - slow_apply["Pyro"] - quick_apply["Pyro"] == 0:
                            self.comp_name = characters[0] + " Soup"
                        else:
                            self.comp_name = "Overvape " + characters[0]
                    elif CHARACTERS[characters[0]]["element"] == "Hydro" or characters[0] == "Xiangling":
                        if "Xiangling" in characters and "Tartaglia" in characters and "Bennett" in characters and "Kaedehara Kazuha" in characters:
                            self.alt_comp_name = "International Childe"
                        if characters[0] == "Xiangling":
                            for char_name in characters:
                                if CHARACTERS[char_name]["element"] == "Hydro":
                                    self.comp_name = "Reverse Vape " + char_name
                        elif len(dps) < 2:
                            self.comp_name = "Reverse Vape " + characters[0]
                    elif len(dps) < 2 or "Dehya" in dps:
                        self.comp_name = "Vape " + characters[0]
                        if len_element["Pyro"] - slow_apply["Pyro"] > 1:
                            if len(anemo) > 0:
                                self.alt_comp_name = self.comp_name.replace("Vape", "VV Vape")
                            else:
                                self.alt_comp_name = self.comp_name.replace("Vape", "Double Pyro")
                                if len_element["Pyro"] == 3:
                                    self.alt_comp_name = self.comp_name.replace("Vape", "Triple Pyro")
                        elif len_element["Geo"] > 1:
                            self.alt_comp_name = "Double Geo " + characters[0]
                        elif len_element["Anemo"] > 0 and CHARACTERS[characters[0]]["element"] != "Anemo":
                            self.alt_comp_name = self.comp_name.replace("Vape", "VV Vape")
                # elif len_element["Electro"] > 0 and (len(dps) < 2 or "Raiden Shogun" in dps):
                elif len_element["Electro"] > 0 and (len(dps) < 2):
                    self.comp_name = "Overload " + characters[0]
                # elif quick_apply["Cryo"] > 0 and len_element["Pyro"] - slow_apply["Pyro"] - quick_apply["Pyro"] > 0:
                elif quick_apply["Cryo"] > 0:
                    if (quick_apply["Pyro"] > 0 and len_element["Pyro"] - quick_apply["Pyro"] - slow_apply["Pyro"] == 0) or CHARACTERS[characters[0]]["element"] == "Cryo":
                        for char_name in characters:
                            if CHARACTERS[char_name]["element"] == "Cryo":
                                self.comp_name = "Reverse Melt " + char_name
                                break
                    else:
                        self.comp_name = "Melt " + characters[0]
                elif len_element["Pyro"] > 1 and (len(dps) < 2 or characters[0] == "Raiden Shogun"
                    or "Faruzan" in dps or "Sucrose" in dps or "Jean" in dps):
                    if len_element["Geo"] > 1 and (CHARACTERS[characters[0]]["element"] == "Geo" or characters[0] == "Xiangling"):
                        self.comp_name = "Double Geo Double Pyro"
                    else:
                        if (CHARACTERS[characters[0]]["element"] == "Pyro"
                            or CHARACTERS[characters[0]]["element"] == "Anemo"
                            or CHARACTERS[characters[0]]["element"] == "Geo"):
                            self.comp_name = characters[0] + " Hypercarry"
                        else:
                            self.comp_name = "Mono Pyro " + characters[0]
                        self.alt_comp_name = "Double Pyro " + characters[0]
                        if len_element["Pyro"] == 3:
                            self.alt_comp_name = self.comp_name.replace("Double Pyro", "Triple Pyro")
            # No pyro apply, dendro
            elif quick_apply["Cryo"] > 0 and len_element["Hydro"] > 0:
                self.comp_name = "Freeze " + characters[0]
            if self.comp_name == "-":
                if len_element["Hydro"] > 0:
                    if len_element["Electro"] > 0:
                        if "Sangonomiya Kokomi" == characters[0]:
                            self.comp_name = "Tapu Koko"
                        elif len_element["Pyro"] > 0 and len_element["Anemo"] > 0:
                            self.comp_name = characters[0] + " Soup"
                        elif len(dps) < 2 or "Yae Miko" in dps or "Xingqiu" in dps or "Yelan" in dps or "Furina" in dps:
                            self.comp_name = characters[0] + " Taser"
                            if characters[0] in ["Xingqiu", "Yelan", "Furina", "Sucrose"]:
                                self.alt_comp_name = self.comp_name.replace(characters[0], "Quickswap")
                                self.comp_name = "Tapu Koko"
                    elif len_element["Hydro"] > 1:
                        self.comp_name = "Double Hydro " + characters[0]
                        if len_element["Hydro"] == 3:
                            self.alt_comp_name = self.comp_name.replace("Double Hydro", "Triple Hydro")
                        if characters[0] in ["Xingqiu", "Yelan", "Furina", "Sucrose"]:
                            self.comp_name = self.comp_name.replace(characters[0], "Quickswap")
                if self.comp_name == "-":
                    if len_element["Geo"] > 1:
                        self.comp_name = "Double Geo " + characters[0]
                        if len_element["Geo"] == 3:
                            self.alt_comp_name = self.comp_name.replace("Double Geo", "Triple Geo")
                            # if CHARACTERS[characters[0]]["element"] == "Geo":
                            #     self.comp_name = self.comp_name.replace("Double Geo", "Mono Geo")
                    elif len_element["Electro"] > 1 and (len(dps) < 2 or ("Raiden Shogun" in characters and "Yae Miko" in characters)):
                        if "Bennett" in characters and "Raiden Shogun" in characters and anemo:
                            if "Yae Miko" in characters:
                                self.comp_name = "Raikou"
                            else:
                            # elif "Kujou Sara" in characters:
                                self.comp_name = "Raiden Hypercarry"
                        else:
                            self.comp_name = "Double Electro " + characters[0]
                            if len_element["Electro"] == 3:
                                if CHARACTERS[characters[0]]["element"] == "Electro":
                                    self.comp_name = self.comp_name.replace("Double Electro", "Mono Electro")
                                self.alt_comp_name = self.comp_name.replace("Double Electro", "Triple Electro")
                    elif len(dps) == 2 and "Faruzan" not in dps and "Sucrose" not in dps and "Jean" not in dps and "Xingqiu" not in dps:
                        self.comp_name = characters[0] + "/" + characters[1] + " Dual Carry"
                    elif len_element["Cryo"] > 2:
                        self.comp_name = "Double Cryo " + characters[0]
                        if len_element["Cryo"] == 3:
                            self.alt_comp_name = self.comp_name.replace("Double Cryo", "Triple Cryo")
                    elif slow_apply["Pyro"] > 0 and len(anemo) > 0 and CHARACTERS[characters[0]]["element"] == "Cryo":
                        self.comp_name = "Reverse Melt " + characters[0]
                    else:
                        if characters[0] == "Faruzan":
                            self.comp_name = characters[1] + " Hypercarry"
                        else:
                            self.comp_name = characters[0] + " Hypercarry"
            # if self.comp_name == "-":
            #     if len(dps) + len(sub) > 2:
            #         self.comp_name = " Triple Carry" + characters[0]
            #     elif len(dps) + len(sub) > 1:
            #         self.comp_name = " Dual Carry" + characters[0]
            #     elif len(dps) + len(sub) == 1:
            #         if len(anemo) > 1:
            #             self.comp_name = " Hypercarry" + characters[0]
            #         elif len(healer) > 1:
            #             self.comp_name = " Dual Sustain" + characters[0]
        for char_name in [" Shogun", " Miko", "Sangonomiya ", "Kamisato ", "Arataki ", "Kaedehara ", "Shikanoin "]:
            self.comp_name = self.comp_name.replace(char_name, "")
            self.alt_comp_name = self.alt_comp_name.replace(char_name, "")
        self.comp_name = self.comp_name.replace("Tartaglia", "Childe")
        self.alt_comp_name = self.alt_comp_name.replace("Tartaglia", "Childe")
        if info_char and self.alt_comp_name != "-":
            self.comp_name = self.alt_comp_name

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
            if self.elements[ele] > 1:
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
