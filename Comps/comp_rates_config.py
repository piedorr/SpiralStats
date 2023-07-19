import json

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

RECENT_PHASE = "3.8a"
past_phase = "Jul1"
char_infographics = "Klee"

# threshold for comps, not inclusive
global app_rate_threshold
global f2p_app_rate_threshold
app_rate_threshold = 0.2
f2p_app_rate_threshold = 0.2

# threshold for comps in character infographics
global char_app_rate_threshold
char_app_rate_threshold = 0

# archetypes: all, Nilou, dendro, nondendro, off-field, on-field, melt, freeze, hyperbloom, spread
archetype = "all"
whaleCheck = False
whaleCheckOnly = True
whaleSigWeap = False
sigWeaps = []
standWeaps = []

# Char infographics should be separated from overall comp rankings
run_commands = [
    "Char usages all chambers",
    "Comp usage floor 12 combined",
    "Comp usage floor 12 each half",
    "Comp usage floor 11 each half"
]

alt_comps = "Character specific infographics" in run_commands

commands = [
    "Comp usage each chamber",
    "Character specific infographics",
    "Char usages for each chamber"
]