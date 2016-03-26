import os

directory = "arffs/teams/"
files = os.listdir(directory)
f_out = open("arffs/combined_teams.arff", "w")
wrote_headers = False
teams = ""

for f in files:
    f_read = open(directory + f)
    for line in f_read:
        if not wrote_headers:
            if "@attribute" in line:
                f_out.write(line)
            if "@relation" in line:
                f_out.write("@relation NBA_Teams\n")
            if "opponent_id" in line:
                teams = line.split(" ")[2]
            if "@data" in line:
                f_out.write("@attribute team_label " + teams)
                f_out.write("@data\n")
                wrote_headers = True
        else:
            if "@" not in line:
                label = f.split(".")[0].replace(" ", "_")
                f_out.write(line[:-1] + ", " + label + "\n")
