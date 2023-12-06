import json

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)

RECENT_PHASE = "4.2a"
past_phase = "Oct2"

# threshold for comps, not inclusive
global app_rate_threshold
global f2p_app_rate_threshold
app_rate_threshold = 0.5
# f2p_app_rate_threshold = 0.5

char_infographics = ["Furina", "Baizhu", "Charlotte", "Beidou", "Collei", "Cyno", "Kamisato Ayato", "Kirara", "Xiangling", "Kuki Shinobu"]
char_infographics = char_infographics[8]

# threshold for comps in character infographics
global char_app_rate_threshold
char_app_rate_threshold = 0.3

# archetypes: all, Nilou, dendro, nondendro, off-field, on-field, melt, freeze, hyperbloom, spread
archetype = "all"
whaleCheck = True
whaleCheckOnly = True
whaleSigWeap = False
sigWeaps = []
standWeaps = []

# Char infographics should be separated from overall comp rankings
run_commands = [
    "Char usages all chambers", #must be included, also includes duos
    "Comp usage floor 11 each half",
    "Comp usage floor 12 each half",
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
if alt_comps and char_app_rate_threshold > app_rate_threshold:
    app_rate_threshold = char_app_rate_threshold

with open('../data/characters.json') as char_file:
    CHARACTERS = json.load(char_file)
