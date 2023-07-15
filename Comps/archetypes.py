import csv
import json
from comp_rates_config import archetype

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

def find_archetype(foundchar):
    match archetype:
        case "Nilou":
            return(foundchar["foundNilou"])
        case "dendro":
            return(foundchar["foundDendro"])
        case "nondendro":
            return(not foundchar["foundDendro"])
        case "off-field":
            return(not foundchar["foundOnField"] and not foundchar["foundNilou"])
        case "on-field":
            return(foundchar["foundOnField"] and not foundchar["foundNilou"])
        case "melt":
            return(foundchar["foundPyro"])
        case "freeze":
            return(foundchar["foundHydro"] and not foundchar["foundPyro"])
        case "hyperbloom":
            return(foundchar["foundElectro"] and foundchar["foundDendro"] and foundchar["foundHydro"])
        case "spread":
            return(foundchar["foundElectro"] and foundchar["foundDendro"] and not foundchar["foundHydro"])
        case _:
            return(True)

elementChars = {
    # Sucrose, Raiden, Lisa, Kokomi, Yae? Ayato?
    "Pyro": [],
    "Hydro": [],
    "Electro": [],
    "Dendro": [],
    "Nilou": ["Nilou"],
    "OnField": []
}
for char in CHARACTERS:
    if CHARACTERS[char]["element"] == "Pyro":
        elementChars["Pyro"] += [char]
    if CHARACTERS[char]["element"] == "Hydro":
        elementChars["Hydro"] += [char]
    if CHARACTERS[char]["element"] == "Electro":
        elementChars["Electro"] += [char]
    if CHARACTERS[char]["element"] == "Dendro":
        elementChars["Dendro"] += [char]
    if CHARACTERS[char]["on_field"]:
        elementChars["OnField"] += [char]

def resetfind():
    foundchar = {
        "found": False,
        "foundPyro": False,
        "foundHydro": False,
        "foundElectro": False,
        "foundDendro": False,
        "foundNilou": False,
        "foundOnField": False
    }
    return foundchar

def findchars(char, foundchar):
    foundchar["foundPyro"] = char in elementChars["Pyro"] or foundchar["foundPyro"]
    foundchar["foundHydro"] = char in elementChars["Hydro"] or foundchar["foundHydro"]
    foundchar["foundElectro"] = char in elementChars["Electro"] or foundchar["foundElectro"]
    foundchar["foundDendro"] = char in elementChars["Dendro"] or foundchar["foundDendro"]
    foundchar["foundNilou"] = char in elementChars["Nilou"] or foundchar["foundNilou"]
    foundchar["foundOnField"] = char in elementChars["OnField"] or foundchar["foundOnField"]