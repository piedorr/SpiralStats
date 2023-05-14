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

                if character in ["Tartaglia","Kamisato Ayaka","Tighnari","Hu Tao","Xiao","Eula","Arataki Itto","Razor","Diluc","Yoimiya","Keqing","Noelle","Klee","Shikanoin Heizou","Cyno","Wanderer","Alhaitham","Dehya"]:
                    dps.insert(0, character)
                elif character in ["Bennett","Qiqi","Diona","Sayu","Kuki Shinobu","Dori","Layla","Yaoyao","Mika"]:
                    healer.append(character)
                elif character in ["Kaedehara Kazuha","Venti","Traveler-A"]:
                    anemo.append(character)
                elif character in ["Thoma"]:
                    healer.insert(0, character)
                elif character in ["Raiden Shogun"]:
                    dps.append(character)
                elif character in ["Shenhe","Collei","Gorou","Mona","Kujou Sara","Rosaria","Fischl","Kaeya","Yun Jin","Traveler-G","Aloy","Traveler-E","Xinyan","Traveler-D","Candace","Nahida"]:
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
                    "Jean" in temp or
                    "Kaedehara Kazuha" in anemo or
                    "Venti" in anemo or
                    "Faruzan" in temp
                ) and "Bennett" in healer and "Xiao" in dps:
                    healer.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    healer.insert(0, character)
                    temp_remove.append(character)
                    continue
            elif character in ["Faruzan"]:
                if "Wanderer" in dps or "Xiao" in dps:
                    dps.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    sub.append(character)
                    temp_remove.append(character)
                    continue
            elif character in ["Nilou"]:
                if "Nahida" in sub:
                    sub.append(character)
                    temp_remove.append(character)
                    continue
                else:
                    dps.insert(0, character)
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
                if "Dehya" in dps and character in ["Ganyu"]:
                    dps.insert(0, character)
                    temp_remove.append(character)
                    continue
                elif character in ["Ningguang","Ganyu","Kamisato Ayato"]:
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
        if "Nahida" in sub:
            if not(dps):
                sub.remove("Nahida")
                dps.append("Nahida")
            elif "Raiden Shogun" in dps and ("Yae Miko" in dps or len(dps) == 1):
                sub.remove("Nahida")
                dps.insert(0, "Nahida")
                dps.remove("Raiden Shogun")
                sub.insert(0, "Raiden Shogun")
                if "Kamisato Ayato" in sub:
                    sub.remove("Kamisato Ayato")
                    dps.insert(0, "Kamisato Ayato")
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
                    # For Sukokomon, where Kokomi is DPS and Xiangling+Fischl is sub
                    if "Fischl" in sub and "Xiangling" in temp:
                        dps.append(character)
                        temp_remove.append(character)
                        continue
                    else:
                        anemo.append(character)
                        temp_remove.append(character)
                        continue
                if healer and "Zhongli" not in healer:
                    if character in ["Sangonomiya Kokomi","Lisa"]:
                        sub.append(character)
                        temp_remove.append(character)
                        continue
                else:
                    if character in ["Sangonomiya Kokomi","Lisa"]:
                        sub.append(character)
                        temp_remove.append(character)
                        continue
            else:
                if character in ["Sangonomiya Kokomi","Lisa"]:
                    if "Yae Miko" in sub:
                        sub.append(character)
                        temp_remove.append(character)
                        continue
                    else:
                        dps.insert(0, character)
                        temp_remove.append(character)
                        continue

        for character in temp_remove:
            temp.remove(character)
        for character in temp:
            if character in ["Sucrose"]:
                if "Xiangling" in sub or "Yae Miko" in sub:
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
                print("dps: " + str(dps) + ", sub: " + str(sub) + ", anemo: " + str(anemo) + ", healer: " + str(healer))
                print("not included: " + str(temp))
        self.fivecount = len(fives)
        self.characters = dps + sub + anemo + healer

    def name_structs(self, characters):
        """Name structure creator.
        """
        comp_names = {
            # Quickbloom: kokomi/barbara, dendro, electro, dendro/anemo/electro
            "Quickbloom Ningguang": [
                ["Ningguang","Yae Miko","Nahida","Sangonomiya Kokomi"],
                ["Ningguang","Nahida","Sangonomiya Kokomi","Kuki Shinobu"]
            ],
            "Quickbloom Kokomi": [
                # Alt: Quickbloom Raiden, Yae
                ["Raiden Shogun","Traveler-D","Fischl","Sangonomiya Kokomi"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Zhongli"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Sangonomiya Kokomi"],
                ["Sangonomiya Kokomi","Traveler-D","Sucrose","Kuki Shinobu"],
                ["Sangonomiya Kokomi","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Sangonomiya Kokomi","Traveler-D","Fischl","Sucrose"],
                ["Sangonomiya Kokomi","Traveler-D","Collei","Kuki Shinobu"],
                ["Yae Miko","Fischl","Sangonomiya Kokomi","Venti"],
                ["Yae Miko","Traveler-D","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Quickbloom Tighnari": [
                ["Tighnari","Nahida","Barbara","Kuki Shinobu"],
                ["Tighnari","Yelan","Nahida","Kuki Shinobu"],
                ["Tighnari","Raiden Shogun","Nahida","Sangonomiya Kokomi"],
                ["Tighnari","Fischl","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Tighnari","Yae Miko","Nahida","Sangonomiya Kokomi"],
                ["Tighnari","Yae Miko","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Quickbloom Alhaitham": [
                ["Alhaitham","Nahida","Fischl","Sangonomiya Kokomi"],
                ["Alhaitham","Nahida","Sangonomiya Kokomi","Kuki Shinobu"],
                ["Alhaitham","Raiden Shogun","Nahida","Sangonomiya Kokomi"],
                ["Alhaitham","Yae Miko","Nahida","Sangonomiya Kokomi"]
            ],
            "Quickbloom Cyno": [
                ["Cyno","Traveler-D","Fischl","Sangonomiya Kokomi"],
                ["Cyno","Nahida","Fischl","Sangonomiya Kokomi"]
            ],
            "Quickbloom Keqing": [
                ["Keqing","Traveler-D","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Keqing","Traveler-D","Fischl","Sangonomiya Kokomi"],
                ["Keqing","Nahida","Fischl","Sangonomiya Kokomi"],
                ["Keqing","Nahida","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Quickbloom Nahida": [
                ["Nahida","Raiden Shogun","Traveler-D","Sangonomiya Kokomi"],
                ["Nahida","Raiden Shogun","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Nahida","Raiden Shogun","Sangonomiya Kokomi","Venti"],
                ["Nahida","Raiden Shogun","Sangonomiya Kokomi","Zhongli"],
                ["Nahida","Raiden Shogun","Fischl","Sangonomiya Kokomi"],
                ["Nahida","Raiden Shogun","Kaedehara Kazuha","Barbara"],
                ["Nahida","Raiden Shogun","Ningguang","Sangonomiya Kokomi"],
                ["Nahida","Yun Jin","Sangonomiya Kokomi","Kuki Shinobu"],
                ["Nahida","Sangonomiya Kokomi","Zhongli","Kuki Shinobu"],
                ["Nahida","Sangonomiya Kokomi","Venti","Kuki Shinobu"],
                ["Nahida","Sangonomiya Kokomi","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Sangonomiya Kokomi","Sucrose","Kuki Shinobu"],
                ["Nahida","Fischl","Sangonomiya Kokomi","Sucrose"],
                ["Nahida","Fischl","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Nahida","Fischl","Beidou","Sangonomiya Kokomi"],
                ["Nahida","Yae Miko","Raiden Shogun","Sangonomiya Kokomi"],
                ["Nahida","Yae Miko","Sangonomiya Kokomi","Kuki Shinobu"],
                ["Nahida","Yae Miko","Sangonomiya Kokomi","Venti"],
                ["Nahida","Yae Miko","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Nahida","Yae Miko","Sangonomiya Kokomi","Zhongli"],
                ["Nahida","Yae Miko","Fischl","Sangonomiya Kokomi"]
            ],

            # Hyperbloom: Quick hydro app (must be Xingqiu/Yelan/Ayato, not Kokomi NAs), dendro, electro, flex
            # With pyro: Unless there's an infused character on-field (usually Nahida/Cyno) and the pyro's Bennett, put in Curry
            # Unless it's Thoma, which is really meant to go curry
            # With quick cryo (not Diona): Hyperfridge
            "Hyperbloom Hu Tao": [
                ["Hu Tao","Xingqiu","Nahida","Kuki Shinobu"]
            ],
            "Hyperbloom Wanderer": [
                ["Wanderer","Xingqiu","Nahida","Kuki Shinobu"]
            ],
            "Hyperbloom Quickswap": [
                ["Raiden Shogun","Xingqiu","Traveler-D","Zhongli"],
                ["Raiden Shogun","Xingqiu","Traveler-D","Fischl"],
                ["Raiden Shogun","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Raiden Shogun","Xingqiu","Traveler-D","Kaedehara Kazuha"],
                ["Raiden Shogun","Xingqiu","Traveler-D","Jean"],
                ["Raiden Shogun","Xingqiu","Traveler-D","Yaoyao"],
                ["Raiden Shogun","Yelan","Traveler-D","Zhongli"],
                ["Raiden Shogun","Yelan","Traveler-D","Jean"],
                ["Raiden Shogun","Yelan","Traveler-D","Yaoyao"],
                ["Raiden Shogun","Yelan","Traveler-D","Sangonomiya Kokomi"],
                ["Raiden Shogun","Yelan","Xingqiu","Traveler-D"],
                ["Raiden Shogun","Yelan","Xingqiu","Yaoyao"],
                ["Raiden Shogun","Yelan","Collei","Jean"],
                ["Lisa","Xingqiu","Traveler-D","Fischl"],
                ["Lisa","Xingqiu","Nahida","Fischl"],
                ["Sucrose","Xingqiu","Traveler-D","Fischl"],
                ["Sucrose","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Sucrose","Xingqiu","Fischl","Collei"],
                ["Sucrose","Xingqiu","Fischl","Yaoyao"],
                ["Sucrose","Xingqiu","Nahida","Fischl"],
                ["Sucrose","Xingqiu","Nahida","Kuki Shinobu"],
                ["Sucrose","Yelan","Traveler-D","Kuki Shinobu"],
                ["Xingqiu","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Xingqiu","Traveler-D","Fischl","Kuki Shinobu"],
                ["Xingqiu","Traveler-D","Collei","Kuki Shinobu"],
                ["Xingqiu","Traveler-D","Zhongli","Kuki Shinobu"],
                ["Yelan","Traveler-D","Kaedehara Kazuha","Kuki Shinobu"],
                ["Yelan","Xingqiu","Kuki Shinobu","Yaoyao"],
                ["Yelan","Xingqiu","Traveler-D","Kuki Shinobu"]
            ],
            "Hyperbloom Ningguang": [
                ["Ningguang","Xingqiu","Nahida","Kuki Shinobu"],
                ["Ningguang","Yelan","Nahida","Kuki Shinobu"]
            ],
            "Hyperbloom Noelle": [
                ["Noelle","Raiden Shogun","Xingqiu","Nahida"],
                ["Noelle","Xingqiu","Nahida","Fischl"]
            ],
            "Hyperbloom Cyno": [
                ["Cyno","Xingqiu","Traveler-D","Beidou"],
                ["Cyno","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Cyno","Xingqiu","Traveler-D","Fischl"],
                ["Cyno","Xingqiu","Nahida","Bennett"],
                ["Cyno","Xingqiu","Nahida","Kuki Shinobu"],
                ["Cyno","Xingqiu","Nahida","Zhongli"],
                ["Cyno","Xingqiu","Nahida","Beidou"],
                ["Cyno","Xingqiu","Nahida","Yaoyao"],
                ["Cyno","Yelan","Xingqiu","Nahida"],
                ["Cyno","Yelan","Traveler-D","Kuki Shinobu"],
                ["Cyno","Yelan","Traveler-D","Zhongli"],
                ["Cyno","Yelan","Nahida","Yaoyao"],
                ["Cyno","Yelan","Nahida","Kuki Shinobu"],
                ["Cyno","Yelan","Nahida","Zhongli"]
            ],
            "Hyperbloom Keqing": [
                ["Keqing","Xingqiu","Nahida","Kuki Shinobu"],
                ["Keqing","Yelan","Nahida","Zhongli"]
            ],
            "Hyperbloom Ayato": [
                ["Raiden Shogun","Kamisato Ayato","Kaedehara Kazuha","Yaoyao"],
                ["Kamisato Ayato","Xingqiu","Nahida","Kuki Shinobu"],
                ["Kamisato Ayato","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Kamisato Ayato","Yelan","Nahida","Kuki Shinobu"],
                ["Kamisato Ayato","Yelan","Traveler-D","Kuki Shinobu"],
                ["Kamisato Ayato","Yae Miko","Nahida","Zhongli"],
                ["Kamisato Ayato","Yun Jin","Nahida","Kuki Shinobu"],
                ["Kamisato Ayato","Collei","Kaedehara Kazuha","Kuki Shinobu"],
                ["Kamisato Ayato","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Kamisato Ayato","Traveler-D","Venti","Kuki Shinobu"],
                ["Kamisato Ayato","Traveler-D","Collei","Kuki Shinobu"],
                ["Kamisato Ayato","Traveler-D","Nahida","Kuki Shinobu"],
                ["Kamisato Ayato","Nahida","Raiden Shogun","Yaoyao"],
                ["Kamisato Ayato","Nahida","Raiden Shogun","Zhongli"],
                ["Kamisato Ayato","Nahida","Beidou","Kuki Shinobu"],
                ["Kamisato Ayato","Nahida","Zhongli","Kuki Shinobu"],
                ["Kamisato Ayato","Nahida","Fischl","Kuki Shinobu"],
                ["Kamisato Ayato","Nahida","Fischl","Zhongli"],
                ["Kamisato Ayato","Nahida","Kaedehara Kazuha","Kuki Shinobu"],
                ["Kamisato Ayato","Nahida","Venti","Kuki Shinobu"]
            ],
            "Hyperbloom Nahida": [
                ["Nahida","Raiden Shogun","Xingqiu","Collei"],
                ["Nahida","Raiden Shogun","Xingqiu","Bennett"],
                ["Nahida","Raiden Shogun","Xingqiu","Yaoyao"],
                ["Nahida","Raiden Shogun","Xingqiu","Qiqi"],
                ["Nahida","Raiden Shogun","Xingqiu","Barbara"],
                ["Nahida","Raiden Shogun","Xingqiu","Zhongli"],
                ["Nahida","Raiden Shogun","Xingqiu","Fischl"],
                ["Nahida","Raiden Shogun","Xingqiu","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Xingqiu","Kaedehara Kazuha"],
                ["Nahida","Raiden Shogun","Xingqiu","Jean"],
                ["Nahida","Raiden Shogun","Xingqiu","Venti"],
                ["Nahida","Raiden Shogun","Xingqiu","Beidou"],
                ["Nahida","Raiden Shogun","Xingqiu","Sangonomiya Kokomi"],
                ["Nahida","Raiden Shogun","Xingqiu","Diona"],
                ["Nahida","Raiden Shogun","Yelan","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Yelan","Bennett"],
                ["Nahida","Raiden Shogun","Yelan","Barbara"],
                ["Nahida","Raiden Shogun","Yelan","Zhongli"],
                ["Nahida","Raiden Shogun","Yelan","Venti"],
                ["Nahida","Raiden Shogun","Yelan","Kaedehara Kazuha"],
                ["Nahida","Raiden Shogun","Yelan","Sangonomiya Kokomi"],
                ["Nahida","Raiden Shogun","Yelan","Jean"],
                ["Nahida","Raiden Shogun","Yelan","Yaoyao"],
                ["Nahida","Raiden Shogun","Yelan","Diona"],
                ["Nahida","Raiden Shogun","Yelan","Xingqiu"],
                ["Nahida","Raiden Shogun","Yae Miko","Xingqiu"],
                ["Nahida","Yelan","Xingqiu","Kuki Shinobu"],
                ["Nahida","Yelan","Xingqiu","Fischl"],
                ["Nahida","Yelan","Yae Miko","Venti"],
                ["Nahida","Yelan","Yae Miko","Kuki Shinobu"],
                ["Nahida","Yelan","Yae Miko","Sangonomiya Kokomi"],
                ["Nahida","Yelan","Yae Miko","Zhongli"],
                ["Nahida","Yelan","Yae Miko","Diona"],
                ["Nahida","Yelan","Yae Miko","Bennett"],
                ["Nahida","Yelan","Bennett","Kuki Shinobu"],
                ["Nahida","Yelan","Beidou","Kuki Shinobu"],
                ["Nahida","Yelan","Fischl","Kuki Shinobu"],
                ["Nahida","Yelan","Fischl","Sangonomiya Kokomi"],
                ["Nahida","Yelan","Sucrose","Kuki Shinobu"],
                ["Nahida","Yelan","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Yelan","Mona","Kuki Shinobu"],
                ["Nahida","Yelan","Zhongli","Kuki Shinobu"],
                ["Nahida","Yelan","Sangonomiya Kokomi","Kuki Shinobu"],
                ["Nahida","Yelan","Traveler-D","Kuki Shinobu"],
                ["Nahida","Yelan","Nilou","Kuki Shinobu"],
                ["Nahida","Xingqiu","Venti","Kuki Shinobu"],
                ["Nahida","Xingqiu","Diona","Kuki Shinobu"],
                ["Nahida","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Nahida","Xingqiu","Traveler-A","Kuki Shinobu"],
                ["Nahida","Xingqiu","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Xingqiu","Collei","Kuki Shinobu"],
                ["Nahida","Xingqiu","Zhongli","Kuki Shinobu"],
                ["Nahida","Xingqiu","Beidou","Kuki Shinobu"],
                ["Nahida","Xingqiu","Sangonomiya Kokomi","Kuki Shinobu"],
                ["Nahida","Xingqiu","Sucrose","Kuki Shinobu"],
                ["Nahida","Xingqiu","Fischl","Sangonomiya Kokomi"],
                ["Nahida","Xingqiu","Fischl","Kuki Shinobu"],
                ["Nahida","Xingqiu","Fischl","Kaedehara Kazuha"],
                ["Nahida","Xingqiu","Fischl","Sucrose"],
                ["Nahida","Xingqiu","Fischl","Beidou"],
                ["Nahida","Xingqiu","Kuki Shinobu","Yaoyao"],
                ["Nahida","Barbara","Nilou","Kuki Shinobu"],
                ["Nahida","Yae Miko","Raiden Shogun","Yelan"],
                ["Nahida","Yae Miko","Xingqiu","Sangonomiya Kokomi"],
                ["Nahida","Yae Miko","Xingqiu","Kuki Shinobu"],
                ["Nahida","Yae Miko","Xingqiu","Fischl"]
            ],
            "Hyperbloom Alhaitham": [
                ["Alhaitham","Yelan","Zhongli","Kuki Shinobu"],
                ["Alhaitham","Yelan","Kuki Shinobu","Yaoyao"],
                ["Alhaitham","Yelan","Traveler-D","Kuki Shinobu"],
                ["Alhaitham","Yelan","Xingqiu","Kuki Shinobu"],
                ["Alhaitham","Yelan","Fischl","Zhongli"],
                ["Alhaitham","Yelan","Kaedehara Kazuha","Kuki Shinobu"],
                ["Alhaitham","Yelan","Nahida","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Fischl","Yaoyao"],
                ["Alhaitham","Xingqiu","Fischl","Zhongli"],
                ["Alhaitham","Xingqiu","Fischl","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Collei","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Kaedehara Kazuha","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Zhongli","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Nahida","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Kuki Shinobu","Yaoyao"],
                ["Alhaitham","Xingqiu","Traveler-D","Kuki Shinobu"],
                ["Alhaitham","Xingqiu","Traveler-A","Kuki Shinobu"],
                ["Alhaitham","Raiden Shogun","Xingqiu","Diona"],
                ["Alhaitham","Raiden Shogun","Xingqiu","Yaoyao"],
                ["Alhaitham","Raiden Shogun","Xingqiu","Nahida"],
                ["Alhaitham","Raiden Shogun","Xingqiu","Zhongli"],
                ["Alhaitham","Raiden Shogun","Yelan","Nahida"],
                ["Alhaitham","Raiden Shogun","Yelan","Zhongli"],
                ["Alhaitham","Raiden Shogun","Yelan","Yaoyao"]
            ],
            "Hyperbloom Childe": [
                ["Tartaglia","Yelan","Nahida","Kuki Shinobu"],
                ["Tartaglia","Nahida","Kaedehara Kazuha","Kuki Shinobu"]
            ],
            "Hyperbloom Eula": [
                ["Eula","Yelan","Nahida","Kuki Shinobu"],
                ["Eula","Xingqiu","Nahida","Kuki Shinobu"]
            ],

            # Hyperfridge: Hyperbloom with quick cryo
            "Hyperfridge Ayaka": [
                ["Kamisato Ayaka","Raiden Shogun","Xingqiu","Nahida"],
                ["Kamisato Ayaka","Yae Miko","Nahida","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Xingqiu","Nahida","Kuki Shinobu"]
            ],
            "Hyperfridge Nahida": [
                ["Ganyu","Yelan","Nahida","Kuki Shinobu"],
                ["Nahida","Xingqiu","Kuki Shinobu","Layla"],
                ["Nahida","Xingqiu","Kaeya","Kuki Shinobu"]
            ],

            # Curry: Pyro, electro, dendro, hydro, like soup but with vegetables
            # Raiden/Kuki doesn't work (go to hyperbloom), only Fischl/Beidou
            # Unless it's Thoma, which is really meant to go curry
            "Raiden Curry": [
                ["Raiden Shogun","Xingqiu","Traveler-D","Bennett"],
                ["Raiden Shogun","Xingqiu","Collei","Bennett"],
                ["Raiden Shogun","Yelan","Traveler-D","Bennett"]
            ],
            "Thundering Furry": [
                ["Razor","Xingqiu","Traveler-D","Bennett"],
                ["Razor","Xingqiu","Nahida","Bennett"]
            ],
            "Chaos Cyno": [
                ["Cyno","Yelan","Nahida","Thoma"]
            ],
            "Nahida Curry": [
                ["Nahida","Xingqiu","Fischl","Thoma"],
                ["Nahida","Xingqiu","Fischl","Bennett"],
                ["Nahida","Xingqiu","Thoma","Kuki Shinobu"]
            ],

            # Bloom: Dendro, anemo and hydro only (Bennett as the only pyro possible)
            # Alt: Bloom with other on-field chars
            "Bloom Alhaitham": [
                ["Nilou","Alhaitham","Xingqiu","Yaoyao"],
                ["Alhaitham","Nahida","Nilou","Sangonomiya Kokomi"]
            ],
            "Bloom Ayato": [
                ["Nilou","Kamisato Ayato","Traveler-D","Yaoyao"],
                ["Kamisato Ayato","Nahida","Nilou","Yaoyao"]
            ],
            "Bloom Tighnari": [
                ["Tighnari","Nilou","Traveler-D","Sangonomiya Kokomi"],
                ["Tighnari","Nilou","Nahida","Sangonomiya Kokomi"]
            ],
            "Bloom Ayato": [
                ["Kamisato Ayato","Traveler-D","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Nahida","Kaedehara Kazuha","Bennett"]
            ],
            "Bloom Childe": [
                ["Tartaglia","Nahida","Nilou","Yaoyao"],
                ["Tartaglia","Nahida","Kaedehara Kazuha","Bennett"]
            ],
            "Bloom Nilou": [
                ["Kamisato Ayato","Traveler-D","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Nahida","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Nahida","Nilou","Yaoyao"],
                ["Tartaglia","Nahida","Nilou","Yaoyao"],
                ["Tartaglia","Nahida","Kaedehara Kazuha","Bennett"],
                ["Alhaitham","Nahida","Nilou","Sangonomiya Kokomi"],
                ["Tighnari","Nilou","Nahida","Sangonomiya Kokomi"],
                ["Tighnari","Nilou","Traveler-D","Sangonomiya Kokomi"],
                ["Nilou","Alhaitham","Xingqiu","Yaoyao"],
                ["Nilou","Kamisato Ayato","Traveler-D","Yaoyao"],
                ["Nilou","Traveler-D","Collei","Sangonomiya Kokomi"],
                ["Nilou","Traveler-D","Collei","Barbara"],
                ["Nilou","Traveler-D","Sangonomiya Kokomi","Yaoyao"],
                ["Nilou","Traveler-D","Barbara","Yaoyao"],
                ["Nilou","Collei","Traveler-A","Barbara"],
                ["Nilou","Collei","Sangonomiya Kokomi","Traveler-A"],
                ["Nilou","Collei","Sangonomiya Kokomi","Yaoyao"],
                ["Nilou","Yelan","Traveler-D","Sangonomiya Kokomi"],
                ["Nilou","Yelan","Traveler-D","Barbara"],
                ["Nilou","Yelan","Traveler-D","Yaoyao"],
                ["Nahida","Yelan","Xingqiu","Nilou"],
                ["Nilou","Xingqiu","Traveler-D","Sangonomiya Kokomi"],
                ["Nilou","Xingqiu","Traveler-D","Collei"],
                ["Nilou","Xingqiu","Traveler-D","Yaoyao"],
                ["Nahida","Yelan","Nilou","Sangonomiya Kokomi"],
                ["Nahida","Yelan","Nilou","Barbara"],
                ["Nahida","Yelan","Nilou","Yaoyao"],
                ["Nahida","Xingqiu","Nilou","Sangonomiya Kokomi"],
                ["Nahida","Xingqiu","Nilou","Barbara"],
                ["Nahida","Xingqiu","Nilou","Yaoyao"],
                ["Nahida","Xingqiu","Mona","Nilou"],
                ["Nahida","Nilou","Sangonomiya Kokomi","Barbara"],
                ["Nahida","Nilou","Sangonomiya Kokomi","Traveler-A"],
                ["Nahida","Nilou","Sangonomiya Kokomi","Yaoyao"],
                ["Nahida","Nilou","Traveler-A","Barbara"],
                ["Nahida","Barbara","Nilou","Yaoyao"],
                ["Nahida","Candace","Nilou","Yaoyao"],
                ["Nahida","Traveler-D","Nilou","Sangonomiya Kokomi"],
                ["Nahida","Traveler-D","Nilou","Barbara"],
                ["Nahida","Traveler-D","Nilou","Yaoyao"],
                ["Nahida","Collei","Nilou","Yaoyao"],
                ["Nahida","Collei","Nilou","Sangonomiya Kokomi"],
                ["Nahida","Collei","Nilou","Barbara"]
            ],
            "Reverse Vape Nilou": [
                ["Nilou","Xiangling","Kaedehara Kazuha","Bennett"]
            ],

            # Burning: Dendro, Pyro, flex no hydro
            # Alternate: Overburn
            "Overburn Raiden": [
                ["Raiden Shogun","Xiangling","Traveler-D","Bennett"],
                ["Raiden Shogun","Xiangling","Collei","Bennett"]
            ],
            "Burning Nahida": [
            # Alternate: Overburn
                ["Nahida","Xiangling","Bennett","Diona"],
                ["Nahida","Xiangling","Raiden Shogun","Bennett"],
                ["Nahida","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Nahida","Kaedehara Kazuha","Venti","Bennett"],
                ["Nahida","Raiden Shogun","Bennett","Layla"]
            ],
            "Burning Dehya": [
                ["Dehya","Nahida","Kaedehara Kazuha","Bennett"]
            ],

            # Burgeon: Dendro, Hydro, Pyro, flex no electro/pyro/cryo
            "Burgeon Quickswap": [
                ["Xingqiu","Traveler-D","Kaedehara Kazuha","Bennett"]
            ],
            "Burgeon Hu Tao": [
                ["Hu Tao","Xingqiu","Nahida","Zhongli"],
                ["Hu Tao","Xingqiu","Nahida","Diona"],
                ["Hu Tao","Xingqiu","Collei","Zhongli"],
                ["Hu Tao","Xingqiu","Traveler-D","Zhongli"],
                ["Hu Tao","Yelan","Xingqiu","Nahida"],
                ["Hu Tao","Yelan","Nahida","Zhongli"]
            ],
            "Burgeon Klee": [
                ["Klee","Xingqiu","Nahida","Zhongli"]
            ],
            "Burgeon Diluc": [
                ["Diluc","Xingqiu","Nahida","Zhongli"]
            ],
            "Burgeon Dehya": [
                ["Dehya","Yelan","Nahida","Sangonomiya Kokomi"]
            ],
            "Burgeon Yoimiya": [
                ["Yoimiya","Yelan","Nahida","Zhongli"],
                ["Yoimiya","Xingqiu","Nahida","Zhongli"]
            ],
            "Burgeon Nahida": [
                ["Nahida","Yelan","Sangonomiya Kokomi","Thoma"],
                ["Nahida","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Nahida","Xiangling","Xingqiu","Bennett"],
                ["Nahida","Xiangling","Xingqiu","Zhongli"]
            ],

            # Spread: Dendro main, electro, no hydro
            "Spread Tighnari": [
                ["Tighnari","Yae Miko","Fischl","Kaedehara Kazuha"],
                ["Tighnari","Yae Miko","Fischl","Yaoyao"],
                ["Tighnari","Yae Miko","Fischl","Zhongli"],
                ["Tighnari","Yae Miko","Nahida","Kuki Shinobu"],
                ["Tighnari","Yae Miko","Nahida","Fischl"],
                ["Tighnari","Yae Miko","Nahida","Zhongli"],
                ["Tighnari","Yae Miko","Traveler-D","Zhongli"],
                ["Tighnari","Yae Miko","Traveler-D","Diona"],
                ["Tighnari","Yae Miko","Zhongli","Yaoyao"],
                ["Tighnari","Yae Miko","Kaedehara Kazuha","Zhongli"],
                ["Tighnari","Raiden Shogun","Nahida","Zhongli"],
                ["Tighnari","Raiden Shogun","Yae Miko","Zhongli"],
                ["Tighnari","Raiden Shogun","Nahida","Kuki Shinobu"],
                ["Tighnari","Raiden Shogun","Kaedehara Kazuha","Bennett"],
                ["Tighnari","Nahida","Fischl","Zhongli"],
                ["Tighnari","Nahida","Zhongli","Kuki Shinobu"],
                ["Tighnari","Nahida","Fischl","Kuki Shinobu"],
                ["Tighnari","Nahida","Kaedehara Kazuha","Kuki Shinobu"],
                ["Tighnari","Fischl","Kaedehara Kazuha","Kuki Shinobu"],
                ["Tighnari","Fischl","Kaedehara Kazuha","Zhongli"],
                ["Tighnari","Keqing","Fischl","Zhongli"],
                ["Tighnari","Traveler-D","Fischl","Zhongli"]
            ],
            "Spread Alhaitham": [
                ["Alhaitham","Nahida","Kuki Shinobu","Yaoyao"],
                ["Alhaitham","Nahida","Beidou","Kuki Shinobu"],
                ["Alhaitham","Nahida","Zhongli","Kuki Shinobu"],
                ["Alhaitham","Nahida","Fischl","Kuki Shinobu"],
                ["Alhaitham","Nahida","Fischl","Zhongli"],
                ["Alhaitham","Raiden Shogun","Nahida","Yaoyao"],
                ["Alhaitham","Raiden Shogun","Nahida","Zhongli"],
                ["Alhaitham","Raiden Shogun","Nahida","Kuki Shinobu"],
                ["Alhaitham","Raiden Shogun","Yae Miko","Zhongli"],
                ["Alhaitham","Raiden Shogun","Traveler-D","Zhongli"],
                ["Alhaitham","Fischl","Zhongli","Yaoyao"],
                ["Alhaitham","Fischl","Collei","Zhongli"],
                ["Alhaitham","Fischl","Beidou","Yaoyao"],
                ["Alhaitham","Yae Miko","Kaedehara Kazuha","Zhongli"],
                ["Alhaitham","Yae Miko","Zhongli","Yaoyao"],
                ["Alhaitham","Yae Miko","Fischl","Yaoyao"],
                ["Alhaitham","Yae Miko","Fischl","Zhongli"],
                ["Alhaitham","Yae Miko","Nahida","Diona"],
                ["Alhaitham","Yae Miko","Nahida","Yaoyao"],
                ["Alhaitham","Yae Miko","Nahida","Zhongli"],
                ["Alhaitham","Yae Miko","Nahida","Fischl"],
                ["Alhaitham","Yae Miko","Nahida","Kuki Shinobu"]
            ],
            "Spread Nahida": [
                ["Nahida","Fischl","Beidou","Kaedehara Kazuha"],
                ["Nahida","Fischl","Beidou","Venti"],
                ["Nahida","Fischl","Beidou","Zhongli"],
                ["Nahida","Fischl","Beidou","Sucrose"],
                ["Nahida","Fischl","Lisa","Kaedehara Kazuha"],
                ["Nahida","Fischl","Kaedehara Kazuha","Bennett"],
                ["Nahida","Fischl","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Venti","Zhongli"],
                ["Nahida","Raiden Shogun","Venti","Bennett"],
                ["Nahida","Raiden Shogun","Venti","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Venti","Yaoyao"],
                ["Nahida","Raiden Shogun","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Kaedehara Kazuha","Zhongli"],
                ["Nahida","Raiden Shogun","Kaedehara Kazuha","Bennett"],
                ["Nahida","Raiden Shogun","Kaedehara Kazuha","Diona"],
                ["Nahida","Raiden Shogun","Fischl","Zhongli"],
                ["Nahida","Raiden Shogun","Fischl","Venti"],
                ["Nahida","Raiden Shogun","Fischl","Bennett"],
                ["Nahida","Raiden Shogun","Fischl","Kaedehara Kazuha"],
                ["Nahida","Raiden Shogun","Fischl","Jean"],
                ["Nahida","Raiden Shogun","Fischl","Sucrose"],
                ["Nahida","Raiden Shogun","Kujou Sara","Zhongli"],
                ["Nahida","Raiden Shogun","Kujou Sara","Kaedehara Kazuha"],
                ["Nahida","Raiden Shogun","Kujou Sara","Bennett"],
                ["Nahida","Raiden Shogun","Kujou Sara","Jean"],
                ["Nahida","Raiden Shogun","Kujou Sara","Kuki Shinobu"],
                ["Nahida","Raiden Shogun","Zhongli","Bennett"],
                ["Nahida","Yae Miko","Raiden Shogun","Zhongli"],
                ["Nahida","Yae Miko","Raiden Shogun","Bennett"],
                ["Nahida","Yae Miko","Raiden Shogun","Sucrose"],
                ["Nahida","Yae Miko","Raiden Shogun","Jean"],
                ["Nahida","Yae Miko","Raiden Shogun","Kaedehara Kazuha"],
                ["Nahida","Yae Miko","Raiden Shogun","Venti"],
                ["Nahida","Yae Miko","Raiden Shogun","Yaoyao"],
                ["Nahida","Yae Miko","Raiden Shogun","Diona"],
                ["Nahida","Yae Miko","Fischl","Kuki Shinobu"],
                ["Nahida","Yae Miko","Fischl","Yaoyao"],
                ["Nahida","Yae Miko","Fischl","Zhongli"],
                ["Nahida","Yae Miko","Fischl","Kaedehara Kazuha"],
                ["Nahida","Yae Miko","Fischl","Jean"],
                ["Nahida","Yae Miko","Fischl","Sucrose"],
                ["Nahida","Yae Miko","Fischl","Bennett"],
                ["Nahida","Yae Miko","Kaedehara Kazuha","Yaoyao"],
                ["Nahida","Yae Miko","Kaedehara Kazuha","Kuki Shinobu"],
                ["Nahida","Yae Miko","Kaedehara Kazuha","Bennett"],
                ["Nahida","Yae Miko","Kaedehara Kazuha","Zhongli"],
                ["Nahida","Yae Miko","Venti","Zhongli"],
                ["Nahida","Yae Miko","Venti","Kuki Shinobu"],
                ["Nahida","Yae Miko","Jean","Zhongli"],
                ["Nahida","Yae Miko","Sucrose","Kuki Shinobu"],
                ["Nahida","Yae Miko","Zhongli","Kuki Shinobu"],
                ["Nahida","Yae Miko","Traveler-D","Diona"],
                ["Nahida","Yae Miko","Traveler-D","Zhongli"],
                ["Nahida","Yae Miko","Kujou Sara","Zhongli"],
                ["Nahida","Yae Miko","Kuki Shinobu","Yaoyao"],
                ["Ganyu","Nahida","Zhongli","Kuki Shinobu"]
            ],

            # Aggravate: electro main, dendro, no hydro
            "Aggravate Quickswap": [
                # Alt: Aggravate Raiden, Sucrose
                ["Fischl","Kaedehara Kazuha","Venti","Yaoyao"],
                ["Sucrose","Fischl","Beidou","Yaoyao"],
                ["Sucrose","Traveler-D","Fischl","Beidou"],
                ["Raiden Shogun","Traveler-D","Sucrose","Yaoyao"],
                ["Raiden Shogun","Traveler-D","Zhongli","Bennett"],
                ["Raiden Shogun","Traveler-D","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Traveler-D","Fischl","Zhongli"],
                ["Raiden Shogun","Traveler-D","Fischl","Venti"],
                ["Raiden Shogun","Traveler-D","Kujou Sara","Bennett"],
                ["Raiden Shogun","Kujou Sara","Kaedehara Kazuha","Yaoyao"],
                ["Raiden Shogun","Kujou Sara","Collei","Jean"],
                ["Raiden Shogun","Collei","Kaedehara Kazuha","Bennett"],
                ["Traveler-D","Fischl","Beidou","Kaedehara Kazuha"],
                ["Traveler-D","Fischl","Kaedehara Kazuha","Bennett"]
            ],
            "Aggravate Heizou": [
                ["Shikanoin Heizou","Yae Miko","Fischl","Collei"]
            ],
            "Aggravate Lisa": [
                ["Lisa","Traveler-D","Fischl","Sucrose"],
                ["Lisa","Nahida","Fischl","Sucrose"]
            ],
            "Aggravate Keqing": [
                ["Keqing","Traveler-D","Fischl","Jean"],
                ["Keqing","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Keqing","Traveler-D","Fischl","Sucrose"],
                ["Keqing","Traveler-D","Fischl","Zhongli"],
                ["Keqing","Traveler-D","Fischl","Venti"],
                ["Keqing","Traveler-D","Kaedehara Kazuha","Zhongli"],
                ["Keqing","Traveler-D","Kaedehara Kazuha","Kuki Shinobu"],
                ["Keqing","Nahida","Kujou Sara","Zhongli"],
                ["Keqing","Nahida","Kujou Sara","Kaedehara Kazuha"],
                ["Keqing","Nahida","Fischl","Kaedehara Kazuha"],
                ["Keqing","Nahida","Fischl","Sucrose"],
                ["Keqing","Nahida","Fischl","Zhongli"],
                ["Keqing","Nahida","Fischl","Venti"],
                ["Keqing","Nahida","Fischl","Kuki Shinobu"],
                ["Keqing","Nahida","Fischl","Jean"],
                ["Keqing","Nahida","Fischl","Yaoyao"],
                ["Keqing","Nahida","Venti","Bennett"],
                ["Keqing","Nahida","Kaedehara Kazuha","Zhongli"],
                ["Keqing","Nahida","Kaedehara Kazuha","Bennett"],
                ["Keqing","Nahida","Kaedehara Kazuha","Kuki Shinobu"],
                ["Keqing","Collei","Kaedehara Kazuha","Kuki Shinobu"],
                ["Keqing","Yae Miko","Nahida","Zhongli"],
                ["Keqing","Yae Miko","Nahida","Jean"],
                ["Keqing","Fischl","Sucrose","Yaoyao"],
                ["Keqing","Fischl","Kaedehara Kazuha","Yaoyao"],
                ["Keqing","Fischl","Traveler-A","Zhongli"],
                ["Keqing","Fischl","Venti","Yaoyao"],
                ["Keqing","Fischl","Collei","Kaedehara Kazuha"],
                ["Keqing","Fischl","Collei","Sucrose"],
                ["Keqing","Fischl","Collei","Zhongli"]
            ],
            "Aggravate Yae": [
                ["Raiden Shogun","Yae Miko","Venti","Yaoyao"],
                ["Raiden Shogun","Yae Miko","Kaedehara Kazuha","Yaoyao"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Zhongli"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Bennett"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Kaedehara Kazuha"],
                ["Yae Miko","Fischl","Kaedehara Kazuha","Yaoyao"],
                ["Yae Miko","Fischl","Sucrose","Yaoyao"],
                ["Yae Miko","Traveler-D","Fischl","Zhongli"],
                ["Yae Miko","Traveler-D","Fischl","Sucrose"],
                ["Yae Miko","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Yae Miko","Traveler-D","Sucrose","Bennett"],
                ["Yae Miko","Traveler-D","Kaedehara Kazuha","Kuki Shinobu"],
                ["Yae Miko","Nahida","Fischl","Sucrose"],
                ["Yae Miko","Nahida","Fischl","Kaedehara Kazuha"],
                ["Yae Miko","Nahida","Sucrose","Bennett"],
                ["Yae Miko","Nahida","Kaedehara Kazuha","Kuki Shinobu"]
            ],
            "Aggravate Cyno": [
                ["Cyno","Nahida","Zhongli","Dori"],
                ["Cyno","Nahida","Beidou","Zhongli"],
                ["Cyno","Nahida","Fischl","Zhongli"],
                ["Cyno","Nahida","Fischl","Kaedehara Kazuha"],
                ["Cyno","Nahida","Sucrose","Kuki Shinobu"],
                ["Cyno","Nahida","Kaedehara Kazuha","Kuki Shinobu"],
                ["Cyno","Nahida","Kaedehara Kazuha","Zhongli"],
                ["Cyno","Nahida","Albedo","Zhongli"],
                ["Cyno","Traveler-D","Fischl","Zhongli"],
                ["Cyno","Traveler-D","Fischl","Kaedehara Kazuha"],
                ["Cyno","Traveler-D","Sucrose","Kuki Shinobu"],
                ["Cyno","Traveler-D","Kaedehara Kazuha","Kuki Shinobu"],
                ["Cyno","Traveler-D","Albedo","Zhongli"],
                ["Cyno","Fischl","Collei","Zhongli"],
                ["Cyno","Yae Miko","Traveler-D","Zhongli"],
                ["Cyno","Yae Miko","Nahida","Zhongli"]
            ],

            "Freeze Ganyu": [
            # Alt: Morgana
                ["Ganyu","Mona","Venti","Layla"],
                ["Ganyu","Mona","Venti","Diona"],
                ["Ganyu","Mona","Kaedehara Kazuha","Diona"],
                ["Ganyu","Mona","Kaedehara Kazuha","Venti"],
                ["Ganyu","Mona","Sucrose","Diona"],
                ["Ganyu","Mona","Venti","Zhongli"],
                ["Ganyu","Kamisato Ayato","Venti","Diona"],
                ["Ganyu","Kamisato Ayato","Kaedehara Kazuha","Diona"],
                ["Ganyu","Sangonomiya Kokomi","Venti","Diona"],
                ["Ganyu","Sangonomiya Kokomi","Kaedehara Kazuha","Zhongli"],
                ["Ganyu","Sangonomiya Kokomi","Kaedehara Kazuha","Diona"],
                ["Ganyu","Shenhe","Mona","Venti"],
                ["Ganyu","Shenhe","Mona","Kaedehara Kazuha"],
                ["Ganyu","Shenhe","Mona","Diona"],
                ["Ganyu","Shenhe","Sangonomiya Kokomi","Venti"],
                ["Ganyu","Shenhe","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Ganyu","Kaeya","Sangonomiya Kokomi","Venti"],
                ["Ganyu","Rosaria","Mona","Venti"],
                ["Ganyu","Rosaria","Mona","Zhongli"],
                ["Ganyu","Rosaria","Sangonomiya Kokomi","Venti"],
                ["Ganyu","Rosaria","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Ganyu","Rosaria","Kaedehara Kazuha","Zhongli"],
                ["Ganyu","Ningguang","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Freeze Ayaka": [
            # Alt: Moryana, Freeze Ayaka/Ayato, Ayaka/Ganyu, freeze kokomi
                ["Kamisato Ayaka","Sangonomiya Kokomi","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Sangonomiya Kokomi","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayaka","Sangonomiya Kokomi","Venti","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Venti","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Sucrose","Diona"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Mona"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Jean"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Ganyu","Mona","Diona"],
                ["Kamisato Ayaka","Ganyu","Mona","Venti"],
                ["Kamisato Ayaka","Ganyu","Mona","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Mona","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Mona","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Diona"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Shenhe","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Mona","Diona"],
                ["Kamisato Ayaka","Shenhe","Mona","Venti"],
                ["Kamisato Ayaka","Shenhe","Mona","Sucrose"],
                ["Kamisato Ayaka","Shenhe","Mona","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Mona","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Barbara"],
                ["Kamisato Ayaka","Kaeya","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Rosaria","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Rosaria","Mona","Diona"],
                ["Kamisato Ayaka","Rosaria","Mona","Venti"],
                ["Kamisato Ayaka","Rosaria","Mona","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Mona","Venti","Diona"],
                ["Kamisato Ayaka","Mona","Kaedehara Kazuha","Layla"],
                ["Kamisato Ayaka","Mona","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Mona","Sucrose","Diona"],
                ["Kamisato Ayaka","Mona","Zhongli","Diona"],
                ["Kamisato Ayaka","Mona","Venti","Zhongli"],
                ["Kamisato Ayaka","Xingqiu","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Xingqiu","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Xingqiu","Shenhe","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Xingqiu","Rosaria","Zhongli"],
                ["Kamisato Ayaka","Yelan","Ganyu","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Yelan","Xingqiu","Shenhe"],
                ["Kamisato Ayaka","Yelan","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Yelan","Kaedehara Kazuha","Layla"],
                ["Kamisato Ayaka","Yelan","Kaedehara Kazuha","Qiqi"],
                ["Kamisato Ayaka","Yelan","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Yelan","Shenhe","Venti"],
                ["Kamisato Ayaka","Yelan","Shenhe","Diona"],
                ["Kamisato Ayaka","Yelan","Shenhe","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Yelan","Shenhe","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Yelan","Shenhe","Jean"],
                ["Kamisato Ayaka","Yelan","Rosaria","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Yelan","Rosaria","Zhongli"],
                ["Kamisato Ayaka","Barbara","Kaedehara Kazuha","Diona"],
                ["Sangonomiya Kokomi","Shenhe","Rosaria","Kaedehara Kazuha"]
            ],
            "Ayaka Fridge": [
                ["Kamisato Ayaka","Collei","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Ganyu Fridge": [
                ["Ganyu","Nahida","Sangonomiya Kokomi","Venti"]
            ],
            "Mono Cryo Ayaka": [
            # Alt: Ayaka/Ganyu
                ["Kamisato Ayaka","Ganyu","Shenhe","Jean"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Venti"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Diona"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Ganyu","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Ganyu","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Layla"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Rosaria","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayaka","Rosaria","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Kaeya","Kaedehara Kazuha","Diona"]
            ],
            "Mono Cryo Ganyu": [
            # Alt: Ganyu, Ganyu Double Geo
                ["Ganyu","Kaedehara Kazuha","Albedo","Zhongli"],
                ["Ganyu","Shenhe","Kaedehara Kazuha","Layla"],
                ["Ganyu","Shenhe","Kaedehara Kazuha","Diona"],
                ["Ganyu","Shenhe","Kaedehara Kazuha","Zhongli"]
            ],

            "Raiden National Team": [
            # Alt: Vape Kokomi
                ["Xiangling","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Xingqiu","Sucrose","Bennett"],
                ["Xiangling","Xingqiu","Venti","Bennett"],
                ["Xiangling","Xingqiu","Zhongli","Bennett"],
                ["Xiangling","Xingqiu","Rosaria","Bennett"],
                ["Xiangling","Xingqiu","Chongyun","Bennett"],
                ["Xiangling","Xingqiu","Fischl","Bennett"],
                ["Xiangling","Yelan","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Yelan","Sucrose","Bennett"],
                ["Xiangling","Yelan","Venti","Bennett"],
                ["Xiangling","Yelan","Rosaria","Bennett"],
                ["Xiangling","Yelan","Zhongli","Bennett"],
                ["Xiangling","Yelan","Chongyun","Bennett"],
                ["Raiden Shogun","Xiangling","Xingqiu","Bennett"],
                ["Raiden Shogun","Xiangling","Yelan","Bennett"],
                ["Raiden Shogun","Xiangling","Mona","Bennett"],
                ["Shikanoin Heizou","Xiangling","Xingqiu","Bennett"],
                ["Shikanoin Heizou","Xiangling","Yelan","Bennett"],
                ["Cyno","Xiangling","Xingqiu","Bennett"],
                ["Ningguang","Xiangling","Xingqiu","Bennett"],
                ["Xiangling","Xingqiu","Albedo","Bennett"],
                ["Kamisato Ayaka","Xiangling","Xingqiu","Bennett"],
                ["Sangonomiya Kokomi","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Wanderer","Xiangling","Xingqiu","Bennett"]
            ],
            "Raiden Soup": [
            # Raiden, hydro, anemo, pyro
            # Alt: double hydro, sunfire
                ["Raiden Shogun","Kamisato Ayato","Venti","Bennett"],
                ["Raiden Shogun","Kamisato Ayato","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Kamisato Ayato","Sucrose","Bennett"],
                ["Raiden Shogun","Sangonomiya Kokomi","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Xingqiu","Venti","Bennett"],
                ["Raiden Shogun","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Xingqiu","Sucrose","Bennett"],
                ["Raiden Shogun","Xingqiu","Jean","Bennett"],
                ["Raiden Shogun","Yelan","Jean","Bennett"],
                ["Raiden Shogun","Yelan","Venti","Bennett"],
                ["Raiden Shogun","Yelan","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Yelan","Sucrose","Bennett"],
                ["Raiden Shogun","Xiangling","Xingqiu","Sucrose"],
                ["Raiden Shogun","Xiangling","Yelan","Sucrose"],
                ["Raiden Shogun","Xiangling","Xingqiu","Kaedehara Kazuha"],
                ["Raiden Shogun","Mona","Venti","Bennett"],
                ["Raiden Shogun","Mona","Kaedehara Kazuha","Bennett"]
            ],
            "Raiden Hypercarry": [
            # Raiden, Sara, anemo, Bennett
            # Alt: sunfire
                ["Raiden Shogun","Kujou Sara","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Kujou Sara","Kaedehara Kazuha","Zhongli"],
                ["Raiden Shogun","Kujou Sara","Sucrose","Bennett"],
                ["Raiden Shogun","Kujou Sara","Venti","Bennett"],
                ["Raiden Shogun","Kujou Sara","Jean","Bennett"],
                ["Raiden Shogun","Kujou Sara","Zhongli","Bennett"],
                ["Raiden Shogun","Fischl","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Venti","Zhongli","Bennett"],
                ["Raiden Shogun","Kaedehara Kazuha","Zhongli","Bennett"]
            ],
            "Raiden Taser": [
            # Raiden, hydro, no other suitable comps (dendro, sunfire, anemo+pyro)
            # If there's Kokomi, put in Tapu Koko
            # Alt: Double Hydro
                ["Raiden Shogun","Yae Miko","Xingqiu","Sucrose"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Venti"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Bennett"],
                ["Raiden Shogun","Yae Miko","Yelan","Sucrose"],
                ["Raiden Shogun","Yae Miko","Yelan","Venti"],
                ["Raiden Shogun","Yae Miko","Yelan","Jean"],
                ["Raiden Shogun","Yae Miko","Yelan","Bennett"],
                ["Raiden Shogun","Xingqiu","Fischl","Sucrose"],
                ["Raiden Shogun","Xingqiu","Fischl","Bennett"],
                ["Raiden Shogun","Xingqiu","Kujou Sara","Kaedehara Kazuha"],
                ["Raiden Shogun","Xingqiu","Kujou Sara","Bennett"],
                ["Raiden Shogun","Xingqiu","Kaedehara Kazuha","Zhongli"],
                ["Raiden Shogun","Xingqiu","Venti","Zhongli"],
                ["Raiden Shogun","Xingqiu","Venti","Barbara"],
                ["Raiden Shogun","Xingqiu","Sucrose","Barbara"],
                ["Raiden Shogun","Xingqiu","Traveler-A","Zhongli"],
                ["Raiden Shogun","Xingqiu","Mona","Bennett"],
                ["Raiden Shogun","Xingqiu","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Yelan","Fischl","Sucrose"],
                ["Raiden Shogun","Yelan","Fischl","Bennett"],
                ["Raiden Shogun","Yelan","Kujou Sara","Bennett"],
                ["Raiden Shogun","Yelan","Kujou Sara","Jean"],
                ["Raiden Shogun","Yelan","Kujou Sara","Kaedehara Kazuha"],
                ["Raiden Shogun","Yelan","Kujou Sara","Venti"],
                ["Raiden Shogun","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Raiden Shogun","Yelan","Kaedehara Kazuha","Diona"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Venti","Zhongli"],
                ["Raiden Shogun","Yelan","Venti","Barbara"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Jean","Kaedehara Kazuha"],
                ["Raiden Shogun","Yelan","Mona","Bennett"],
                ["Raiden Shogun","Yelan","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Yelan","Xingqiu","Jean"],
                ["Raiden Shogun","Yelan","Xingqiu","Venti"],
                ["Raiden Shogun","Yelan","Xingqiu","Zhongli"],
                ["Raiden Shogun","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Raiden Shogun","Yelan","Xingqiu","Bennett"]
            ],
            # Yae Taser: if there's kokomi, choose tapu koko instead
            "Overvape Raiden/Ayato": [
                ["Raiden Shogun","Kamisato Ayato","Xiangling","Bennett"]
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
            "Raikou": [
            # Raiden, Yae, anemo, Bennett
            # Alt: Raiden Sunfire
                ["Raiden Shogun","Yae Miko","Jean","Bennett"],
                ["Raiden Shogun","Yae Miko","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Yae Miko","Sucrose","Bennett"],
                ["Raiden Shogun","Yae Miko","Venti","Bennett"]
            ],
            "Mono Electro": [
            # electro and anemo only
                ["Raiden Shogun","Yae Miko","Jean","Venti"],
                ["Raiden Shogun","Yae Miko","Kujou Sara","Jean"],
                ["Raiden Shogun","Yae Miko","Kujou Sara","Kaedehara Kazuha"],
                ["Raiden Shogun","Yae Miko","Kaedehara Kazuha","Zhongli"],
                ["Raiden Shogun","Yae Miko","Venti","Zhongli"]
            ],
            "Wanderer Hypercarry": [
                # No reactions
                ["Wanderer","Faruzan","Yanfei","Bennett"],
                ["Wanderer","Faruzan","Thoma","Bennett"],
                ["Wanderer","Faruzan","Zhongli","Bennett"],
                ["Wanderer","Faruzan","Venti","Thoma"],
                ["Wanderer","Faruzan","Venti","Bennett"],
                ["Wanderer","Faruzan","Kaedehara Kazuha","Bennett"],
                ["Wanderer","Faruzan","Yelan","Zhongli"],
                ["Wanderer","Faruzan","Yelan","Bennett"],
                ["Wanderer","Faruzan","Yelan","Diona"],
                ["Wanderer","Faruzan","Xingqiu","Bennett"],
                ["Wanderer","Faruzan","Xingqiu","Zhongli"],
                ["Wanderer","Faruzan","Yun Jin","Bennett"],
                ["Wanderer","Faruzan","Bennett","Layla"],
                ["Wanderer","Faruzan","Bennett","Diona"],
                ["Wanderer","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Wanderer","Yelan","Zhongli","Bennett"],
                ["Wanderer","Venti","Zhongli","Bennett"],
                ["Wanderer","Venti","Albedo","Zhongli"]
            ],
            "Double Pyro Wanderer": [
                ["Wanderer","Dehya","Yelan","Bennett"],
                ["Wanderer","Faruzan","Xiangling","Bennett"],
                ["Wanderer","Xiangling","Zhongli","Bennett"]
            ],
            "Double Geo Xiao": [
                ["Xiao","Faruzan","Albedo","Zhongli"],
                ["Xiao","Jean","Albedo","Zhongli"],
                ["Xiao","Jean","Traveler-G","Zhongli"],
                ["Xiao","Sucrose","Albedo","Zhongli"],
                ["Xiao","Venti","Albedo","Zhongli"],
                ["Xiao","Albedo","Zhongli","Bennett"]
            ],
            "Xiao Hypercarry": [
            # Alt: xiao succ benny dong, sunfire, 3 anemo
                ["Xiao","Faruzan","Bennett","Zhongli"],
                ["Xiao","Faruzan","Kaedehara Kazuha","Bennett"],
                ["Xiao","Faruzan","Jean","Bennett"],
                ["Xiao","Faruzan","Jean","Zhongli"],
                ["Xiao","Sucrose","Bennett","Zhongli"],
                ["Xiao","Kaedehara Kazuha","Bennett","Zhongli"],
                ["Xiao","Venti","Bennett","Zhongli"],
                ["Xiao","Jean","Bennett","Zhongli"]
            ],
            "Double Pyro Xiao": [
                ["Xiao","Faruzan","Xiangling","Bennett"],
                ["Xiao","Sucrose","Xiangling","Bennett"],
                ["Xiao","Xiangling","Zhongli","Bennett"],
                ["Xiao","Xiangling","Venti","Bennett"],
                ["Xiao","Xiangling","Kaedehara Kazuha","Bennett"]
            ],
            "Xiao/Raiden Dual Carry": [
                ["Xiao","Raiden Shogun","Xiangling","Bennett"],
                ["Xiao","Raiden Shogun","Zhongli","Bennett"]
            ],
            "Cyno/Raiden Dual Carry": [
                ["Cyno","Raiden Shogun","Traveler-D","Zhongli"],
                ["Cyno","Raiden Shogun","Nahida","Zhongli"]
            ],
            "Mono Geo Itto": [
            # Alt: 3 geo
                ["Arataki Itto","Mona","Gorou","Zhongli"],
                ["Arataki Itto","Traveler-G","Gorou","Zhongli"],
                ["Arataki Itto","Ningguang","Gorou","Zhongli"],
                ["Arataki Itto","Albedo","Zhongli","Bennett"],
                ["Arataki Itto","Ningguang","Gorou","Qiqi"],
                ["Arataki Itto","Gorou","Albedo","Zhongli"],
                ["Arataki Itto","Gorou","Kaedehara Kazuha","Zhongli"],
                ["Arataki Itto","Gorou","Zhongli","Bennett"],
                ["Arataki Itto","Gorou","Albedo","Bennett"],
                ["Arataki Itto","Gorou","Albedo","Kuki Shinobu"],
                ["Arataki Itto","Gorou","Albedo","Diona"],
                ["Arataki Itto","Gorou","Fischl","Zhongli"],
                ["Arataki Itto","Gorou","Albedo","Sangonomiya Kokomi"],
                ["Arataki Itto","Gorou","Jean","Zhongli"],
                ["Arataki Itto","Gorou","Sangonomiya Kokomi","Zhongli"]
            ],
            "Mono Geo Noelle": [
            # Alt: 3 geo
                ["Noelle","Gorou","Albedo","Zhongli"],
                ["Noelle","Yun Jin","Gorou","Albedo"],
                ["Noelle","Yun Jin","Gorou","Fischl"],
                ["Noelle","Yelan","Gorou","Albedo"],
                ["Noelle","Yelan","Yun Jin","Gorou"],
                ["Noelle","Gorou","Albedo","Sucrose"],
                ["Noelle","Gorou","Fischl","Albedo"]
            ],
            "Triple Geo Ningguang": [
                ["Ningguang","Albedo","Zhongli","Bennett"]
            ],
            "Double Geo Double Pyro": [
                ["Xiangling","Albedo","Zhongli","Bennett"],
                ["Ningguang","Xiangling","Zhongli","Bennett"]
            ],
            "Double Geo Hu Tao": [
                ["Hu Tao","Xingqiu","Albedo","Zhongli"],
                ["Hu Tao","Xingqiu","Ningguang","Zhongli"],
                ["Hu Tao","Xingqiu","Traveler-G","Zhongli"],
                ["Hu Tao","Yelan","Albedo","Zhongli"],
                ["Hu Tao","Yelan","Ningguang","Zhongli"]
            ],
            "Double Hydro Hu Tao": [
                ["Hu Tao","Dehya","Yelan","Xingqiu"],
                ["Hu Tao","Xiangling","Xingqiu","Mona"],
                ["Hu Tao","Yelan","Xingqiu","Yanfei"],
                ["Hu Tao","Yelan","Xingqiu","Jean"],
                ["Hu Tao","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Xingqiu","Sucrose"],
                ["Hu Tao","Yelan","Xingqiu","Zhongli"],
                ["Hu Tao","Yelan","Xingqiu","Albedo"],
                ["Hu Tao","Yelan","Xingqiu","Bennett"],
                ["Hu Tao","Yelan","Xingqiu","Thoma"],
                ["Hu Tao","Yelan","Xingqiu","Diona"],
                ["Hu Tao","Yelan","Xingqiu","Fischl"],
                ["Hu Tao","Yelan","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Sangonomiya Kokomi","Zhongli"],
                ["Hu Tao","Yelan","Mona","Zhongli"],
                ["Hu Tao","Xingqiu","Mona","Zhongli"],
                ["Hu Tao","Xingqiu","Mona","Diona"]
            ],
            "VapeMelt Hu Tao": [
            # cryo subDPS/Layla
                ["Hu Tao","Xingqiu","Ganyu","Zhongli"],
                ["Hu Tao","Xingqiu","Ganyu","Diona"],
                ["Hu Tao","Xingqiu","Chongyun","Zhongli"],
                ["Hu Tao","Xingqiu","Rosaria","Diona"],
                ["Hu Tao","Xingqiu","Rosaria","Zhongli"],
                ["Hu Tao","Xingqiu","Kaeya","Diona"],
                ["Hu Tao","Xingqiu","Mona","Layla"],
                ["Hu Tao","Yelan","Xingqiu","Layla"],
                ["Hu Tao","Yelan","Mona","Layla"],
                ["Hu Tao","Yelan","Ganyu","Zhongli"],
                ["Hu Tao","Yelan","Rosaria","Diona"],
                ["Hu Tao","Yelan","Rosaria","Zhongli"]
            ],
            "Vape Hu Tao": [
            # Hu Tao, Xingqiu, no other suitable comps
            # Alt: double/triple pyro, vv vape
                ["Hu Tao","Xingqiu","Albedo","Diona"],
                ["Hu Tao","Xingqiu","Venti","Zhongli"],
                ["Hu Tao","Xingqiu","Zhongli","Bennett"],
                ["Hu Tao","Xingqiu","Yun Jin","Zhongli"],
                ["Hu Tao","Xingqiu","Sucrose","Zhongli"],
                ["Hu Tao","Xingqiu","Sucrose","Diona"],
                ["Hu Tao","Xingqiu","Sucrose","Bennett"],
                ["Hu Tao","Xingqiu","Sucrose","Thoma"],
                ["Hu Tao","Xingqiu","Sucrose","Yanfei"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Zhongli"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Diona"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Thoma"],
                ["Hu Tao","Xingqiu","Amber","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Sucrose","Bennett"],
                ["Hu Tao","Yelan","Sucrose","Thoma"],
                ["Hu Tao","Yelan","Sucrose","Zhongli"],
                ["Hu Tao","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Hu Tao","Yelan","Venti","Zhongli"],
                ["Hu Tao","Yelan","Chongyun","Zhongli"],
                ["Hu Tao","Yelan","Zhongli","Bennett"],
                ["Hu Tao","Yelan","Sucrose","Diona"],
                ["Hu Tao","Yelan","Kaedehara Kazuha","Bennett"],
                ["Hu Tao","Mona","Kaedehara Kazuha","Bennett"],
                ["Hu Tao","Xiangling","Xingqiu","Zhongli"],
                ["Hu Tao","Xiangling","Yelan","Zhongli"],
                ["Hu Tao","Xiangling","Xingqiu","Diona"],
                ["Hu Tao","Xiangling","Yelan","Bennett"],
                ["Hu Tao","Xiangling","Xingqiu","Bennett"]
            ],
            "Melt Hu Tao": [
                ["Hu Tao","Ganyu","Shenhe","Zhongli"],
                ["Hu Tao","Ganyu","Albedo","Zhongli"],
                ["Hu Tao","Rosaria","Sucrose","Bennett"]
            ],
            "Mono Pyro Hu Tao": [
                ["Hu Tao","Xiangling","Zhongli","Bennett"],
                ["Hu Tao","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Hu Tao","Xiangling","Sucrose","Bennett"]
            ],
            "Funerational": [
                ["Hu Tao","Xiangling","Yelan","Xingqiu"]
            ],
            "Overvape Hu Tao": [
                ["Hu Tao","Xingqiu","Fischl","Zhongli"],
                ["Hu Tao","Xingqiu","Fischl","Diona"],
                ["Hu Tao","Xingqiu","Fischl","Sucrose"],
                ["Hu Tao","Xingqiu","Fischl","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Fischl","Zhongli"],
                ["Hu Tao","Yelan","Xingqiu","Kuki Shinobu"],
                ["Hu Tao","Yae Miko","Xingqiu","Zhongli"],
                ["Hu Tao","Yae Miko","Xingqiu","Diona"],
                ["Hu Tao","Raiden Shogun","Yelan","Zhongli"]
            ],
            "Hu Tao/Raiden Dual Carry": [
                ["Hu Tao","Raiden Shogun","Xingqiu","Bennett"],
                ["Hu Tao","Raiden Shogun","Xingqiu","Zhongli"]
            ],
            "Melt Ayaka": [
            # Alt: melt ayaka/hu tao
                ["Kamisato Ayaka","Ganyu","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayaka","Shenhe","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayaka","Rosaria","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayaka","Dehya","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayaka","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Kamisato Ayaka","Xiangling","Shenhe","Bennett"],
                ["Kamisato Ayaka","Xiangling","Rosaria","Bennett"],
                ["Kamisato Ayaka","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayaka","Xiangling","Zhongli","Bennett"],
                ["Kamisato Ayaka","Hu Tao","Ganyu","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Nahida","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Yelan","Xingqiu"],
                ["Kamisato Ayaka","Hu Tao","Yelan","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Diona"]
            ],
            "Ayato Hypercarry": [
            # Ayato, Yun Jin, anemo, Bennett
            # Alt: 2 hydro, mono hydro
                ["Kamisato Ayato","Yun Jin","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Yun Jin","Venti","Bennett"],
                ["Kamisato Ayato","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayato","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Kamisato Ayato","Yelan","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayato","Yelan","Venti","Bennett"],
                ["Kamisato Ayato","Yelan","Sucrose","Bennett"],
                ["Kamisato Ayato","Yelan","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Xingqiu","Venti","Bennett"],
                ["Kamisato Ayato","Xingqiu","Sucrose","Bennett"],
                ["Kamisato Ayato","Xingqiu","Kaedehara Kazuha","Bennett"]
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
            "Overvape Ayato": [
                ["Kamisato Ayato","Xiangling","Fischl","Bennett"]
            ],
            "Ayato Soup": [
                ["Kamisato Ayato","Fischl","Kaedehara Kazuha","Bennett"]
            ],
            # Ayato, electro, anemo, pyro
            "Ayato Taser": [
            # Ayato, electro, anemo, no pyro
                ["Kamisato Ayato","Fischl","Beidou","Venti"],
                ["Kamisato Ayato","Fischl","Beidou","Sucrose"],
                ["Kamisato Ayato","Fischl","Beidou","Jean"]
            ],
            "International Childe": [
            # Childe, Xiangling, flex, Bennett
            # Alt: rev vape childe, sunfire childe
                ["Tartaglia","Kaedehara Kazuha","Thoma","Bennett"],
                ["Tartaglia","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Tartaglia","Xiangling","Sucrose","Bennett"],
                ["Tartaglia","Xiangling","Venti","Bennett"],
                ["Tartaglia","Xiangling","Zhongli","Bennett"],
                ["Tartaglia","Xiangling","Jean","Bennett"]
            ],
            "Double Hydro Childe": [
            # Alt: Childe taser, mono hydro, double pyro double hydro, double hydro quickswap
                ["Tartaglia","Xingqiu","Venti","Bennett"],
                ["Tartaglia","Xingqiu","Sucrose","Bennett"],
                ["Tartaglia","Xingqiu","Xiangling","Bennett"],
                ["Tartaglia","Xingqiu","Fischl","Beidou"],
                ["Tartaglia","Yelan","Venti","Bennett"],
                ["Tartaglia","Yelan","Sucrose","Bennett"],
                ["Tartaglia","Yelan","Xingqiu","Mona"],
                ["Tartaglia","Mona","Kaedehara Kazuha","Bennett"],
                ["Tartaglia","Yelan","Xiangling","Bennett"],
                ["Xiangling","Yelan","Xingqiu","Bennett"],
                ["Xiangling","Yelan","Xingqiu","Zhongli"],
                ["Xiangling","Yelan","Mona","Kaedehara Kazuha"],
                ["Yelan","Xingqiu","Kaedehara Kazuha","Zhongli"],
                ["Yelan","Xingqiu","Kaedehara Kazuha","Bennett"]
            ],
            "Fireworks Childe": [
                ["Tartaglia","Fischl","Beidou","Bennett"]
            ],
            "Childe/Raiden Dual Carry": [
                ["Tartaglia","Raiden Shogun","Xiangling","Bennett"]
            ],
            "Melt Ganyu": [
                ["Hu Tao","Ganyu","Nahida","Zhongli"],
                ["Ganyu","Venti","Zhongli","Bennett"],
                ["Ganyu","Xiangling","Shenhe","Bennett"],
                ["Ganyu","Xiangling","Zhongli","Bennett"],
                ["Ganyu","Xiangling","Zhongli","Diona"],
                ["Ganyu","Xiangling","Venti","Diona"],
                ["Ganyu","Xiangling","Venti","Bennett"],
                ["Ganyu","Xiangling","Bennett","Diona"],
                ["Ganyu","Xiangling","Kaedehara Kazuha","Zhongli"],
                ["Ganyu","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Ganyu","Xiangling","Sucrose","Bennett"],
                ["Ganyu","Dehya","Xiangling","Bennett"],
                ["Ganyu","Dehya","Kaedehara Kazuha","Bennett"],
                ["Ganyu","Shenhe","Kaedehara Kazuha","Bennett"],
                ["Ganyu","Kaedehara Kazuha","Zhongli","Bennett"]
            ],
            "Burnmelt Ganyu": [
                ["Ganyu","Xiangling","Nahida","Zhongli"],
                ["Ganyu","Nahida","Venti","Bennett"],
                ["Ganyu","Dehya","Nahida","Bennett"],
                ["Ganyu","Nahida","Kaedehara Kazuha","Bennett"],
                ["Ganyu","Nahida","Zhongli","Bennett"]
            ],
            "Eula/Raiden Dual Carry": [
            # Alt: sunfire
                ["Eula","Raiden Shogun","Jean","Bennett"],
                ["Eula","Raiden Shogun","Zhongli","Diona"],
                ["Eula","Raiden Shogun","Zhongli","Bennett"],
                ["Eula","Raiden Shogun","Zhongli","Mika"],
                ["Eula","Raiden Shogun","Venti","Bennett"],
                ["Eula","Raiden Shogun","Venti","Diona"],
                ["Eula","Raiden Shogun","Yelan","Mika"],
                ["Eula","Raiden Shogun","Yelan","Diona"],
                ["Eula","Raiden Shogun","Yelan","Zhongli"],
                ["Eula","Raiden Shogun","Yelan","Bennett"],
                ["Eula","Raiden Shogun","Nahida","Zhongli"],
                ["Eula","Raiden Shogun","Mona","Bennett"],
                ["Eula","Raiden Shogun","Kujou Sara","Jean"],
                ["Eula","Raiden Shogun","Rosaria","Bennett"],
                ["Eula","Raiden Shogun","Rosaria","Jean"],
                ["Eula","Raiden Shogun","Rosaria","Diona"],
                ["Eula","Raiden Shogun","Rosaria","Zhongli"]
            ],
            "Double Electro Eula": [
                ["Eula","Rosaria","Fischl","Kuki Shinobu"],
                ["Eula","Fischl","Beidou","Diona"]
            ],
            "Triple Cryo Eula": [
            # Alt: mono cryo, Eula/Rosaria/Fischl/Zhongli
                ["Eula","Rosaria","Fischl","Diona"],
                ["Eula","Ganyu","Kaedehara Kazuha","Zhongli"],
                ["Eula","Rosaria","Jean","Zhongli"],
                ["Eula","Rosaria","Fischl","Zhongli"]
            ],
            "Vape Yoimiya": [
            # Alt: vv vape, double/triple pyro (xiangling)
                ["Yoimiya","Yelan","Zhongli","Bennett"],
                ["Yoimiya","Yelan","Yun Jin","Zhongli"],
                ["Yoimiya","Yelan","Yun Jin","Bennett"],
                ["Yoimiya","Yelan","Yun Jin","Thoma"],
                ["Yoimiya","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Yoimiya","Xingqiu","Zhongli","Bennett"],
                ["Yoimiya","Xingqiu","Yun Jin","Bennett"],
                ["Yoimiya","Xingqiu","Yun Jin","Zhongli"],
                ["Yoimiya","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Yoimiya","Xingqiu","Sucrose","Bennett"],
                ["Yoimiya","Yelan","Kaedehara Kazuha","Bennett"],
                ["Yoimiya","Xiangling","Xingqiu","Zhongli"],
                ["Yoimiya","Xiangling","Xingqiu","Bennett"],
                ["Yoimiya","Hu Tao","Xingqiu","Zhongli"]
            ],
            "VapeMelt Yoimiya": [
                ["Yoimiya","Yelan","Bennett","Layla"],
                ["Yoimiya","Yelan","Yun Jin","Layla"],
                ["Yoimiya","Xingqiu","Rosaria","Zhongli"]
            ],
            "Overvape Yoimiya": [
                ["Yoimiya","Xingqiu","Beidou","Bennett"],
                ["Yoimiya","Xingqiu","Fischl","Zhongli"],
                ["Yoimiya","Xingqiu","Fischl","Bennett"],
                ["Yoimiya","Yelan","Fischl","Zhongli"]
            ],
            "Double Hydro Yoimiya": [
                ["Yoimiya","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Yoimiya","Yelan","Xingqiu","Sucrose"],
                ["Yoimiya","Yelan","Xingqiu","Zhongli"],
                ["Yoimiya","Yelan","Xingqiu","Bennett"],
                ["Yoimiya","Yelan","Xingqiu","Diona"],
                ["Yoimiya","Xingqiu","Mona","Zhongli"],
                ["Yoimiya","Yelan","Mona","Zhongli"]
            ],
            "Double Geo Yoimiya": [
                ["Yoimiya","Xingqiu","Albedo","Zhongli"],
                ["Yoimiya","Yelan","Albedo","Zhongli"]
            ],
            "Double Electro Yoimiya": [
                ["Yoimiya","Fischl","Beidou","Diona"],
                ["Yoimiya","Xingqiu","Fischl","Beidou"]
            ],
            "Mono Pyro Yoimiya": [
            # Alt: Yoi Hyper
                ["Yoimiya","Xiangling","Zhongli","Bennett"],
                ["Yoimiya","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Yoimiya","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Yoimiya","Yun Jin","Zhongli","Bennett"],
                ["Yoimiya","Yun Jin","Kaedehara Kazuha","Bennett"]
            ],
            "Yoimiya/Raiden Dual Carry": [
                ["Yoimiya","Raiden Shogun","Yelan","Jean"],
                ["Yoimiya","Raiden Shogun","Yelan","Zhongli"],
                ["Yoimiya","Raiden Shogun","Xingqiu","Bennett"],
                ["Yoimiya","Raiden Shogun","Xingqiu","Zhongli"]
            ],
            "Vape Diluc": [
            # Alt: triple pyro
                ["Diluc","Xingqiu","Venti","Bennett"],
                ["Diluc","Xingqiu","Zhongli","Bennett"],
                ["Diluc","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Diluc","Xingqiu","Sucrose","Bennett"],
                ["Diluc","Yelan","Zhongli","Bennett"],
                ["Diluc","Yelan","Kaedehara Kazuha","Bennett"],
                ["Diluc","Yelan","Sucrose","Bennett"],
                ["Diluc","Xiangling","Xingqiu","Bennett"]
            ],
            "Double Geo Diluc": [
                ["Diluc","Xingqiu","Albedo","Zhongli"]
            ],
            "Double Hydro Diluc": [
                ["Diluc","Yelan","Xingqiu","Zhongli"]
            ],
            "Mono Pyro Diluc": [
                ["Diluc","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Diluc","Xiangling","Sucrose","Bennett"]
            ],
            "Vape Dehya": [
                ["Dehya","Mona","Kaedehara Kazuha","Bennett"]
            ],
            "Mono Pyro Dehya": [
                ["Dehya","Xiangling","Kaedehara Kazuha","Bennett"]
            ],
            "Dehya/Raiden Dual Carry": [
                ["Dehya","Raiden Shogun","Kaedehara Kazuha","Bennett"]
            ],
            "Vape Yanfei": [
                ["Yanfei","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Yanfei","Xingqiu","Zhongli","Bennett"],
                ["Yanfei","Xingqiu","Sucrose","Bennett"]
            ],
            "Double Hydro Yanfei": [
                ["Yanfei","Yelan","Xingqiu","Bennett"]
            ],
            "Mono Pyro Yanfei": [
                ["Yanfei","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Yanfei","Xiangling","Sucrose","Bennett"]
            ],
            "Mono Pyro Klee": [
                ["Klee","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Klee","Xiangling","Kaedehara Kazuha","Bennett"],
                ["Klee","Xiangling","Sucrose","Bennett"]
            ],
            "Double Hydro Klee": [
                ["Klee","Yelan","Xingqiu","Bennett"]
            ],
            "Keqing Soup": [
                ["Keqing","Xingqiu","Sucrose","Bennett"]
            ],
            "Keqing Taser": [
                ["Keqing","Fischl","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],


            "Tapu Koko": [
            # Kokomi, electro
            # Alt: taser quickswap, sucrose taser
                ["Sangonomiya Kokomi","Yelan","Fischl","Sucrose"],
                ["Sangonomiya Kokomi","Yae Miko","Fischl","Sucrose"],
                ["Sangonomiya Kokomi","Fischl","Beidou","Sucrose"],
                ["Sangonomiya Kokomi","Fischl","Beidou","Venti"],
                ["Sangonomiya Kokomi","Fischl","Beidou","Kaedehara Kazuha"],
                ["Yae Miko","Fischl","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Yae Miko","Yelan","Sangonomiya Kokomi"],
                ["Raiden Shogun","Yae Miko","Sangonomiya Kokomi","Sucrose"],
                ["Raiden Shogun","Yae Miko","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Yae Miko","Xingqiu","Sangonomiya Kokomi"],
                ["Raiden Shogun","Kujou Sara","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Fischl","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Xingqiu","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Yelan","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Yelan","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Yelan","Xingqiu","Fischl","Beidou"],
                ["Xingqiu","Fischl","Beidou","Kaedehara Kazuha"],
                ["Sucrose","Xingqiu","Fischl","Beidou"],
                ["Sucrose","Yelan","Fischl","Beidou"],
                ["Sucrose","Yelan","Xingqiu","Fischl"],
                ["Sucrose","Fischl","Beidou","Barbara"]
            ],
            "Sukokomon": [
                ["Sangonomiya Kokomi","Sucrose","Xiangling","Fischl"]
            ],
            "Mono Hydro Kokomi": [
                ["Sangonomiya Kokomi","Yelan","Xingqiu","Kaedehara Kazuha"]
            ],

            "Reverse Melt Rosaria": [
            # alt: rev melt chong/kaeya/layla, sunfire
                ["Rosaria","Jean","Bennett","Layla"],
                ["Xiangling","Rosaria","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Rosaria","Kaeya","Bennett"],
                ["Xiangling","Rosaria","Chongyun","Bennett"],
                ["Xiangling","Rosaria","Sucrose","Bennett"],
                ["Xiangling","Rosaria","Bennett","Diona"],
                ["Xiangling","Chongyun","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Kaeya","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Kaeya","Amber","Bennett"],
                ["Xiangling","Kaedehara Kazuha","Bennett","Layla"],
                ["Xiangling","Shenhe","Bennett","Layla"],
                ["Dehya","Rosaria","Kaedehara Kazuha","Bennett"]
            ],
            "Double Electro Kaeya": [
                ["Xingqiu","Lisa","Kaeya","Fischl"]
            ],
            "Mono Pyro Xiangling": [
            # Alt: overload xiangling
                ["Xiangling","Faruzan","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Jean","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Xiangling","Amber","Traveler-A","Bennett"],
                ["Xiangling","Xinyan","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Fischl","Kaedehara Kazuha","Bennett"]
            ],
            "Double Pyro Heizou": [
                ["Shikanoin Heizou","Xiangling","Kaedehara Kazuha","Bennett"]
            ],
            "Double Electro Heizou": [
                ["Shikanoin Heizou","Xingqiu","Fischl","Beidou"]
            ],
            "Double Cryo Heizou": [
                ["Shikanoin Heizou","Xingqiu","Rosaria","Kaeya"]
            ]
        }
        alt_comp_names = {
            "Quickbloom Raiden": [
                ["Raiden Shogun","Traveler-D","Fischl","Sangonomiya Kokomi"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Zhongli"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Raiden Shogun","Traveler-D","Sangonomiya Kokomi","Venti"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Sangonomiya Kokomi"]
            ],
            "Quickbloom Yae": [
                ["Yae Miko","Fischl","Sangonomiya Kokomi","Venti"],
                ["Yae Miko","Traveler-D","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Aggravate Raiden": [
                ["Raiden Shogun","Traveler-D","Sucrose","Yaoyao"],
                ["Raiden Shogun","Traveler-D","Zhongli","Bennett"],
                ["Raiden Shogun","Traveler-D","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Traveler-D","Fischl","Zhongli"],
                ["Raiden Shogun","Traveler-D","Fischl","Venti"],
                ["Raiden Shogun","Traveler-D","Kujou Sara","Bennett"],
                ["Raiden Shogun","Kujou Sara","Collei","Jean"],
                ["Raiden Shogun","Kujou Sara","Kaedehara Kazuha","Yaoyao"],
                ["Raiden Shogun","Collei","Kaedehara Kazuha","Bennett"],
                ["Raiden Shogun","Yae Miko","Venti","Yaoyao"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Zhongli"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Bennett"],
                ["Raiden Shogun","Yae Miko","Traveler-D","Kaedehara Kazuha"]
            ],
            "Aggravate Sucrose": [
                ["Sucrose","Fischl","Beidou","Yaoyao"],
                ["Sucrose","Traveler-D","Fischl","Beidou"]
            ],
            "Overburn Nahida": [
                ["Nahida","Raiden Shogun","Bennett","Layla"],
                ["Nahida","Xiangling","Raiden Shogun","Bennett"]
            ],
            "Morgana": [
                ["Ganyu","Mona","Venti","Layla"],
                ["Ganyu","Mona","Venti","Diona"],
                ["Ganyu","Mona","Kaedehara Kazuha","Diona"],
                ["Ganyu","Mona","Kaedehara Kazuha","Venti"],
                ["Ganyu","Mona","Sucrose","Diona"],
                ["Ganyu","Mona","Venti","Zhongli"]
            ],
            "Moryana": [
                ["Kamisato Ayaka","Rosaria","Mona","Venti"],
                ["Kamisato Ayaka","Rosaria","Mona","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Mona","Venti","Diona"],
                ["Kamisato Ayaka","Mona","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Mona","Sucrose","Diona"],
                ["Kamisato Ayaka","Mona","Zhongli","Diona"],
                ["Kamisato Ayaka","Mona","Venti","Zhongli"]
            ],
            "Freeze Ayaka/Ayato": [
                ["Kamisato Ayaka","Kamisato Ayato","Venti","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Kamisato Ayato","Sucrose","Diona"]
            ],
            "Freeze Ayaka/Ganyu": [
                ["Kamisato Ayaka","Yelan","Ganyu","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Sangonomiya Kokomi"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Mona"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Jean"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Venti"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Sangonomiya Kokomi","Zhongli"],
                ["Kamisato Ayaka","Ganyu","Mona","Diona"],
                ["Kamisato Ayaka","Ganyu","Mona","Venti"],
                ["Kamisato Ayaka","Ganyu","Mona","Sucrose"],
                ["Kamisato Ayaka","Ganyu","Mona","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Mona","Zhongli"]
            ],
            "Mono Cryo Ayaka/Ganyu": [
                ["Kamisato Ayaka","Ganyu","Shenhe","Jean"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Venti"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Kaedehara Kazuha"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Diona"],
                ["Kamisato Ayaka","Ganyu","Shenhe","Zhongli"],
                ["Kamisato Ayaka","Ganyu","Kaedehara Kazuha","Diona"],
                ["Kamisato Ayaka","Ganyu","Kaedehara Kazuha","Zhongli"]
            ],
            "Ganyu Double Geo": [
                ["Ganyu","Kaedehara Kazuha","Albedo","Zhongli"],
            ],
            "Freeze Kokomi": [
                ["Sangonomiya Kokomi","Shenhe","Rosaria","Kaedehara Kazuha"]
            ],
            "Vape Kokomi": [
                ["Sangonomiya Kokomi","Xiangling","Kaedehara Kazuha","Bennett"]
            ],
            "Kazuha National Team": [
                ["Xiangling","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Yelan","Kaedehara Kazuha","Bennett"]
            ],
            "Sucrose National Team": [
                ["Xiangling","Xingqiu","Sucrose","Bennett"],
                ["Xiangling","Yelan","Sucrose","Bennett"]
            ],
            "Rosaria National Team": [
                ["Xiangling","Xingqiu","Rosaria","Bennett"],
                ["Xiangling","Yelan","Rosaria","Bennett"]
            ],
            "Chongyun National Team": [
                ["Xiangling","Xingqiu","Chongyun","Bennett"],
                ["Xiangling","Yelan","Chongyun","Bennett"]
            ],
            "Venti National Team": [
                ["Xiangling","Xingqiu","Venti","Bennett"],
                ["Xiangling","Yelan","Venti","Bennett"]
            ],
            "Fischl National Team": [
                ["Xiangling","Xingqiu","Fischl","Bennett"]
            ],
            "Heizou National Team": [
                ["Shikanoin Heizou","Xiangling","Yelan","Bennett"],
                ["Shikanoin Heizou","Xiangling","Xingqiu","Bennett"]
            ],
            "Ayaka National Team": [
                ["Kamisato Ayaka","Xiangling","Xingqiu","Bennett"]
            ],
            "Cyno National Team": [
                ["Cyno","Xiangling","Xingqiu","Bennett"]
            ],
            "Ningguang National Team": [
                ["Ningguang","Xiangling","Xingqiu","Bennett"]
            ],
            "Zhongli National Team": [
                ["Xiangling","Yelan","Zhongli","Bennett"],
                ["Xiangling","Xingqiu","Zhongli","Bennett"]
            ],
            "Wanderer National Team": [
                ["Wanderer","Xiangling","Xingqiu","Bennett"]
            ],
            "Albedo National Team": [
                ["Xiangling","Xingqiu","Albedo","Bennett"]
            ],
            "Double Hydro Raiden": [
                ["Raiden Shogun","Xingqiu","Venti","Barbara"],
                ["Raiden Shogun","Xingqiu","Sucrose","Barbara"],
                ["Raiden Shogun","Xingqiu","Mona","Bennett"],
                ["Raiden Shogun","Xingqiu","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Venti","Barbara"],
                ["Raiden Shogun","Yelan","Sucrose","Barbara"],
                ["Raiden Shogun","Yelan","Mona","Bennett"],
                ["Raiden Shogun","Yelan","Kamisato Ayato","Bennett"],
                ["Raiden Shogun","Yelan","Xingqiu","Jean"],
                ["Raiden Shogun","Yelan","Xingqiu","Venti"],
                ["Raiden Shogun","Yelan","Xingqiu","Zhongli"],
                ["Raiden Shogun","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Raiden Shogun","Yelan","Xingqiu","Bennett"]
            ],
            "Raiden Sunfire": [
                ["Raiden Shogun","Yae Miko","Jean","Bennett"],
                ["Raiden Shogun","Kujou Sara","Jean","Bennett"],
                ["Raiden Shogun","Xingqiu","Jean","Bennett"],
                ["Raiden Shogun","Yelan","Jean","Bennett"]
            ],
            "Xiao Succ Benny Dong": [
                ["Xiao","Sucrose","Bennett","Zhongli"],
                ["Xiao","Venti","Bennett","Zhongli"]
            ],
            "Xiao Sunfire": [
                ["Xiao","Faruzan","Jean","Bennett"],
                ["Xiao","Jean","Bennett","Zhongli"]
            ],
            "Triple Anemo Xiao": [
                ["Xiao","Faruzan","Kaedehara Kazuha","Bennett"],
                ["Xiao","Faruzan","Jean","Zhongli"]
            ],
            "Triple Geo Itto": [
                ["Arataki Itto","Mona","Gorou","Zhongli"],
                ["Arataki Itto","Raiden Shogun","Gorou","Zhongli"],
                ["Arataki Itto","Albedo","Zhongli","Bennett"],
                ["Arataki Itto","Ningguang","Gorou","Qiqi"],
                ["Arataki Itto","Gorou","Kaedehara Kazuha","Zhongli"],
                ["Arataki Itto","Gorou","Zhongli","Bennett"],
                ["Arataki Itto","Gorou","Albedo","Bennett"],
                ["Arataki Itto","Gorou","Albedo","Kuki Shinobu"],
                ["Arataki Itto","Gorou","Albedo","Diona"],
                ["Arataki Itto","Gorou","Fischl","Zhongli"],
                ["Arataki Itto","Gorou","Fischl","Albedo"],
                ["Arataki Itto","Gorou","Albedo","Sangonomiya Kokomi"],
                ["Arataki Itto","Gorou","Jean","Zhongli"],
                ["Arataki Itto","Gorou","Sangonomiya Kokomi","Zhongli"]
            ],
            "Triple Geo Noelle": [
                ["Noelle","Yun Jin","Gorou","Fischl"],
                ["Noelle","Yelan","Gorou","Albedo"],
                ["Noelle","Yelan","Yun Jin","Gorou"],
                ["Noelle","Gorou","Albedo","Bennett"],
                ["Noelle","Gorou","Albedo","Sucrose"],
                ["Noelle","Gorou","Fischl","Albedo"]
            ],
            "Double Hydro Ayato": [
                ["Kamisato Ayato","Xingqiu","Venti","Bennett"],
                ["Kamisato Ayato","Xingqiu","Sucrose","Bennett"],
                ["Kamisato Ayato","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Kamisato Ayato","Yelan","Venti","Bennett"],
                ["Kamisato Ayato","Yelan","Sucrose","Bennett"],
                ["Kamisato Ayato","Yelan","Kaedehara Kazuha","Zhongli"],
                ["Kamisato Ayato","Yelan","Kaedehara Kazuha","Bennett"]
            ],
            "Mono Hydro Ayato": [
                ["Kamisato Ayato","Yelan","Xingqiu","Kaedehara Kazuha"],
                ["Kamisato Ayato","Yelan","Sangonomiya Kokomi","Kaedehara Kazuha"]
            ],
            "Reverse Vape Childe": [
                ["Tartaglia","Kaedehara Kazuha","Thoma","Bennett"],
                ["Tartaglia","Xiangling","Sucrose","Bennett"],
                ["Tartaglia","Xiangling","Venti","Bennett"],
                ["Tartaglia","Xiangling","Zhongli","Bennett"],
                ["Tartaglia","Xiangling","Jean","Bennett"]
            ],
            "Childe Sunfire": [
                ["Tartaglia","Xiangling","Jean","Bennett"]
            ],
            "Childe Taser": [
                ["Tartaglia","Xingqiu","Fischl","Beidou"]
            ],
            "Mono Hydro Childe": [
                ["Tartaglia","Yelan","Xingqiu","Mona"]
            ],
            "Double Hydro Double Pyro": [
                ["Xiangling","Yelan","Xingqiu","Bennett"],
                ["Tartaglia","Xingqiu","Xiangling","Bennett"],
                ["Tartaglia","Yelan","Xiangling","Bennett"]
            ],
            "Double Hydro Quickswap": [
                ["Xiangling","Yelan","Mona","Kaedehara Kazuha"],
                ["Xiangling","Yelan","Xingqiu","Zhongli"],
                ["Yelan","Xingqiu","Kaedehara Kazuha","Zhongli"],
                ["Yelan","Xingqiu","Kaedehara Kazuha","Bennett"]
            ],
            "Mono Cryo Eula": [
                ["Eula","Ganyu","Kaedehara Kazuha","Zhongli"],
                ["Eula","Rosaria","Jean","Zhongli"]
            ],
            "Eula Sunfire": [
                ["Eula","Raiden Shogun","Jean","Bennett"]
            ],
            "Eula/Rosaria/Fischl/Zhongli": [
                ["Eula","Rosaria","Fischl","Zhongli"]
            ],
            "Yoimiya Hypercarry": [
                ["Yoimiya","Kaedehara Kazuha","Zhongli","Bennett"],
                ["Yoimiya","Yun Jin","Zhongli","Bennett"],
                ["Yoimiya","Yun Jin","Kaedehara Kazuha","Bennett"]
            ],
            "VV Vape Yoimiya": [
                ["Yoimiya","Xingqiu","Kaedehara Kazuha","Bennett"],
                ["Yoimiya","Xingqiu","Sucrose","Bennett"],
                ["Yoimiya","Yelan","Kaedehara Kazuha","Bennett"]
            ],
            "Yoimiya/Hu Tao Dual Carry": [
                ["Yoimiya","Hu Tao","Xingqiu","Zhongli"]
            ],
            "Double Pyro Yoimiya": [
                ["Yoimiya","Xiangling","Xingqiu","Zhongli"]
            ],
            "Triple Pyro Yoimiya": [
                ["Yoimiya","Xiangling","Xingqiu","Bennett"]
            ],
            "Double Pyro Hu Tao": [
                ["Hu Tao","Xiangling","Xingqiu","Zhongli"],
                ["Hu Tao","Xiangling","Yelan","Zhongli"],
                ["Hu Tao","Xiangling","Xingqiu","Diona"]
            ],
            "Triple Pyro Hu Tao": [
                ["Hu Tao","Xiangling","Yelan","Bennett"],
                ["Hu Tao","Xiangling","Xingqiu","Bennett"]
            ],
            "VV Vape Hu Tao": [
            # Hu Tao, Xingqiu, anemo, pyro
                ["Hu Tao","Xingqiu","Sucrose","Bennett"],
                ["Hu Tao","Xingqiu","Sucrose","Thoma"],
                ["Hu Tao","Xingqiu","Sucrose","Yanfei"],
                ["Hu Tao","Xingqiu","Kaedehara Kazuha","Thoma"],
                ["Hu Tao","Xingqiu","Amber","Kaedehara Kazuha"],
                ["Hu Tao","Yelan","Kaedehara Kazuha","Bennett"],
                ["Hu Tao","Yelan","Sucrose","Bennett"],
                ["Hu Tao","Yelan","Sucrose","Thoma"]
            ],
            "Melt Ayaka/Hu Tao": [
                ["Kamisato Ayaka","Hu Tao","Ganyu","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Nahida","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Yelan","Xingqiu"],
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Yelan","Zhongli"],
                ["Kamisato Ayaka","Hu Tao","Xingqiu","Diona"]
            ],
            "Triple Pyro Diluc": [
                ["Diluc","Xiangling","Xingqiu","Bennett"]
            ],
            "Taser Quickswap": [
                ["Yelan","Xingqiu","Fischl","Beidou"],
                ["Xingqiu","Fischl","Beidou","Kaedehara Kazuha"]
            ],
            "Sucrose Taser": [
                ["Sucrose","Xingqiu","Fischl","Beidou"],
                ["Sucrose","Yelan","Fischl","Beidou"],
                ["Sucrose","Yelan","Xingqiu","Fischl"],
                ["Sucrose","Fischl","Beidou","Barbara"]
            ],
            "Overload Xiangling": [
                ["Xiangling","Fischl","Kaedehara Kazuha","Bennett"]
            ],
            "Reverse Melt Chongyun": [
                ["Xiangling","Chongyun","Kaedehara Kazuha","Bennett"]
            ],
            "Reverse Melt Kaeya": [
                ["Xiangling","Kaeya","Kaedehara Kazuha","Bennett"],
                ["Xiangling","Kaeya","Amber","Bennett"]
            ],
            "Rosaria Sunfire": [
                ["Rosaria","Jean","Bennett","Layla"]
            ],
            "Reverse Melt Layla": [
                ["Xiangling","Kaedehara Kazuha","Bennett","Layla"],
                ["Xiangling","Shenhe","Bennett","Layla"]
            ]
        }
        self.comp_name = "-"
        self.alt_comp_name = "-"
        for comp_name in comp_names:
            if characters in comp_names[comp_name]:
                self.comp_name = comp_name
                break
        for alt_comp_name in alt_comp_names:
            if characters in alt_comp_names[alt_comp_name]:
                self.alt_comp_name = alt_comp_name
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
