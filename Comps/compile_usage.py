import csv

phase = ""
phases = []
past_use = {}
past_app = {}
past_own = {}
while phase != "q":
    phase = input("Input folder name(s), or 'q' if done: ")
    if phase != "q":
        phases.append(phase)

for phase in phases:
    with open("../char_results/" + phase + "/12.csv") as stats:
        reader = csv.reader(stats)
        col_names = next(reader)
        past_use[phase] = {}
        past_app[phase] = {}
        past_own[phase] = {}

        for line in reader:
            char_name = line[0]
            match char_name:
                case 'Traveler-A':
                    char_name = "Anemo Traveler"
                case 'Traveler-G':
                    char_name = "Geo Traveler"
                case 'Traveler-E':
                    char_name = "Electro Traveler"
                case 'Traveler-D':
                    char_name = "Dendro Traveler"
                case 'Traveler-H':
                    char_name = "Hydro Traveler"
                case 'Traveler-P':
                    char_name = "Pyro Traveler"
                case 'Traveler-C':
                    char_name = "Cryo Traveler"
                case _:
                    pass
            past_use[phase][char_name] = line[1]
            past_app[phase][char_name] = line[2]
            past_own[phase][char_name] = line[3]

csv_writer_use = csv.writer(open("../char_results/compile_use.csv", 'w', newline=''))
csv_writer_app = csv.writer(open("../char_results/compile_app.csv", 'w', newline=''))
csv_writer_own = csv.writer(open("../char_results/compile_own.csv", 'w', newline=''))
for phase in phases:
    match phase [:3]:
        case "Jan":
            date = "1/"
        case "Feb":
            date = "2/"
        case "Mar":
            date = "3/"
        case "Apr":
            date = "4/"
        case "May":
            date = "5/"
        case "Jun":
            date = "6/"
        case "Jul":
            date = "7/"
        case "Aug":
            date = "8/"
        case "Sep":
            date = "9/"
        case "Oct":
            date = "10/"
        case "Nov":
            date = "11/"
        case "Dec":
            date = "12/"
    if phase[3] == "1":
        date += "1/2023"
    else:
        date += "16/2023"
    for char in past_use[phase]:
        csv_writer_use.writerow([date, char, past_use[phase][char]])
        csv_writer_app.writerow([date, char, past_app[phase][char]])
        csv_writer_own.writerow([date, char, past_own[phase][char]])