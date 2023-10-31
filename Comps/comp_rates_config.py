import json

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

RECENT_PHASE = "4.1b"
past_phase = "Sep1"
char_infographics = ["Neuvillette", "Wriothesley"]
# [0,1,0,-,-,0,-,]
char_infographics = char_infographics[0]

# threshold for comps, not inclusive
global app_rate_threshold
global f2p_app_rate_threshold
app_rate_threshold = 0.5
# f2p_app_rate_threshold = 0.5

# threshold for comps in character infographics
global char_app_rate_threshold
char_app_rate_threshold = 0.4

# archetypes: all, Nilou, dendro, nondendro, off-field, on-field, melt, freeze, hyperbloom, spread
archetype = "all"
whaleCheck = False
whaleCheckOnly = False
whaleSigWeap = False
sigWeaps = []
standWeaps = []

# Char infographics should be separated from overall comp rankings
run_commands = [
    "Char usages all chambers", #must be included, also includes duos
    # "Comp usage floor 11 each half",
    # "Comp usage floor 12 each half",
    # "Character specific infographics",
    # "Comp usage floor 12 combined",
    # "Comp usage each chamber",
    # "Char usages for each chamber",
]

skip_comps = [
    # ("Nahida","Raiden Shogun","Yelan","Sangonomiya Kokomi"),
    # ("Neuvillette","Raiden Shogun","Nahida","Zhongli"),
]




alt_comps = "Character specific infographics" in run_commands

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)
