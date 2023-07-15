import json

# Set class constants in initialization
# Load the list of characters from their file
with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)
with open('../data/artifacts.json') as artifact_file:
    articombinations = json.load(artifact_file)

class PlayerPhase:
    """An object that stores information about a player on a phase. Has:
        player: a string for this player.
        phase: a string for the phase.
        chambers: a string->composition dict for the comps they used.
        owned: a string->dict (character) dict for the characters they owned: 
            None if they don't own the character.
    """

    def __init__(self, player, phase):
        """Composition constructor. Takes in:
            A player, as a string
            A phase, as a string
        """
        self.player = player
        self.phase = phase
        self.owned = {}
        self.chambers = { "11-1-1": None, "11-1-2": None, "11-2-1": None, 
                          "11-2-2": None, "11-3-1": None, "11-3-2": None, 
                          "12-1-1": None, "12-1-2": None, "12-2-1": None, 
                          "12-2-2": None, "12-3-1": None, "12-3-2": None }

    def add_character(self, name, level, cons, weapon, artifacts, element):
        """Adds in a character to the owned characters dict. Takes in:
            A name, a string.
            A level, an integer.
            A cons, an integer.
            A weapon, a string.
            Artifacts, a string.
            Element, a string.
        """

        for arti in articombinations:
            articom = []
            comarti = []
            for artiset in articombinations[arti]:
                articom.append(artiset + ", ")
                comarti.append(", " + artiset)
            for i in articom:
                if i in artifacts:
                    artifacts = artifacts.replace(i, arti + ", ")
            for i in comarti:
                if i in artifacts:
                    artifacts = artifacts.replace(i, "")
                    artifacts = arti + ", " + artifacts

        self.owned[name] = {
            "level": int(level),
            "cons": int(cons),
            "weapon": weapon,
            "artifacts": artifacts,
            "element": element
        }
    
    def add_comp(self, composition):
        """Adds a composition to the chambers dict."""
        if composition.phase != self.phase or composition.player != self.player:
            return
        if self.chambers[composition.room]:
            return
        self.chambers[composition.room] = composition
    
    def chars_owned(self, characters):
        """Takes in an iter of character names, and returns true if the player owned them all."""
        for char in characters:
            if "Traveler" in char:
                continue
            elif char not in self.owned:
                return False
        return True

    def chars_used(self, characters):
        """Takes in an iter of character names, and returns true if the player used them all."""
        if not self.chars_owned(characters):
            return False
        for char in characters:
            if not self.char_used(char):
                return False
        return True

    def no_chars_owned(self, characters):
        """Takes in a list of character names, and returns true if the player owns none of them."""
        for char in characters:
            if self.owned[char]:
                return False
        return True

    def no_chars_used(self, characters):
        """Takes in an iter of character names, and returns true if the player used none of them."""
        for char in characters:
            if self.char_used(char):
                return False
        return True

    def char_used(self, character):
        """Takes in a character name, and returns true if the player used them."""
        if not self.owned[character]:
            return False
        for chamber in self.chambers.values():
            if chamber.char_presence[character]:
                return True
        return False

    def chars_placement(self, characters):
        """Takes in an iter of character names, and if the player owns them all, 
        returns a dict of which chambers each was used in.
        """
        if not self.chars_owned(characters):
            return None
        chambers = { 
            "11-1-1": [], "11-1-2": [], "11-2-1": [], "11-2-2": [], 
            "11-3-1": [], "11-3-2": [], "12-1-1": [], "12-1-2": [], 
            "12-2-1": [], "12-2-2": [], "12-3-1": [], "12-3-2": []
        }
        for char in characters:
            for chamber in chambers:
                if self.chambers[chamber].char_presence[char]:
                    chambers[chamber].append(char)
        return chambers

    def floor_twelve(self):
        """Returns the comps used on floor 12."""
        return [c[1] for c in self.chambers.items() if c[0][:2] == "12"]           
