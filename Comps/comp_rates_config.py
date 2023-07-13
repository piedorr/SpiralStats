import json

# This var needs to change every time
RECENT_PHASE = "2.2b"

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

past_phase = "Jun2"
char = "Razor"

# threshold for comps, not inclusive
global app_rate_threshold
global f2p_app_rate_threshold
app_rate_threshold = 0.2
f2p_app_rate_threshold = 0.2

# threshold for comps in character infographics
global char_app_rate_threshold
char_app_rate_threshold = 0

# archetypes: all, Nilou, dendro, nondendro, off-field, on-field, melt, freeze
# alt_comps = False for char infographics
archetype = "all"
whaleCheck = False
whaleSigWeap = False
sigWeaps = []
standWeaps = []

run_commands = [
    "Char usages all chambers",
    "Character specific infographics"
]

alt_comps = "Character specific infographics" in run_commands

commands = [
    "Comp usage floor 12 each half",
    "Comp usage floor 11 each half",
    "Comp usage floor 12 combined",
    "Comp usage each chamber",
    "Char usages for each chamber"
]