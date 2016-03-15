import os


class PlayerArffToTeamArff:
    def __init__(self, directory):
        self.directory = directory
        files = os.listdir("arffs/very_large_box/")
        self.teams_info = {}
        self.player_files_schema = []
        self.schema_read = False
        for f in files:
            self.process_player_file(f)
        for team in self.teams_info:
            print("\n\nWriting file for team: " + str(team))
            self.teams_info[team].write_file(team)

    def process_player_file(self, filename):
        print("Processing file: " + str(filename))
        player_file = open(self.directory + filename)
        for line in player_file:
            line = line.strip()
            if "@attribute" in line.lower():
                if not self.schema_read:
                    self.player_files_schema.append(line.split()[1])
            elif "@relation" in line.lower() or "@data" in line.lower():
                if "@data" in line.lower():
                    self.schema_read = True
                continue
            else:
                feature_vector = line.split(",")
                # print(line)
                # print("Len feature vector: " + str(len(feature_vector)))
                assert(len(feature_vector) == len(self.player_files_schema))
                assert(self.player_files_schema[9] == "\'team_id\'")
                team_id = feature_vector[9]
                games_info = None
                if team_id in self.teams_info:
                    games_info = self.teams_info.pop(feature_vector[9])
                else:
                    games_info = GamesInfo()

                games_info.add_game_data(feature_vector, self.player_files_schema)
                self.teams_info[team_id] = games_info


class GamesInfo:
    def __init__(self):
        self.games = {}
        self.schema = None

    def add_game_data(self, info, schema):
        assert(schema[0] == "game_id")
        self.schema = schema
        game_id = info[0]

        if game_id in self.games:
            game_stats = self.update_stats(self.games.pop(game_id), info)
            self.games[game_id] = game_stats
        else:
            self.games[game_id] = self.generate_stats(info)

    def update_stats(self, existing, new):
        # schema: fg3a, fg3m, fg3m/a, etc., box minutes, opponent, total players
        total_fg3a = float(existing[0]) + float(new[1])
        total_fg3m = float(existing[1]) + float(new[2])
        average_fg3 = total_fg3m/total_fg3a if total_fg3a > 0 else 0
        total_fga = float(existing[3]) + float(new[3])
        total_fgm = float(existing[4]) + float(new[4])
        average_fg = total_fgm/total_fga if total_fga > 0 else 0
        total_fta = float(existing[6]) + float(new[5])
        total_ftm = float(existing[7]) + float(new[6])
        average_ft = total_ftm/total_fta if total_fta > 0 else 0
        total_minutes = float(existing[9]) + float(new[7])
        opponent = existing[10]
        total_points = float(existing[11]) + float(new[16])
        total_players_accounted = float(existing[12] + 1)
        return (total_fg3a, total_fg3m, average_fg3, total_fga, total_fgm, average_fg, total_fta, total_ftm,
                average_ft, total_minutes, opponent, total_points, total_players_accounted)

    def generate_stats(self, new):
        return new[1], new[2], 0, new[3], new[4], 0, new[5], new[6], 0, new[7], new[8], new[16], 1

    def get_stats_map(self):
        return self.games

    def to_string(self):
        for key in self.games.keys():
            print("Game: " + key)
            print("\t" + str(self.games[key]))

    def write_file(self, name):
        f = open("arffs/teams/" + str(name) + ".arff", 'w')
        f.write("@relation " + str(name) + "\n")

        # schema: game_id, fg3a, fg3m, fg3m/a, etc., box minutes, opponent, total players, average time played
        f.write("@attribute game_id NUMERIC\n")
        f.write("@attribute fg3_attempted_total NUMERIC\n")
        f.write("@attribute fg3_made_total NUMERIC\n")
        f.write("@attribute fg3_percent_average NUMERIC\n")
        f.write("@attribute fg_attempted_total NUMERIC\n")
        f.write("@attribute fg_made_total NUMERIC\n")
        f.write("@attribute fg_percent_average NUMERIC\n")
        f.write("@attribute ft_attempted_total NUMERIC\n")
        f.write("@attribute ft_made_total NUMERIC\n")
        f.write("@attribute ft_percent_average NUMERIC\n")
        f.write("@attribute total_minutes NUMERIC\n")
        f.write("@attribute opponent_id {'1610612737','1610612738','1610612739','1610612740','1610612741',"
                "'1610612742','1610612743','1610612744','1610612745','1610612746','1610612747','1610612748',"
                "'1610612749','1610612750','1610612751','1610612752','1610612753','1610612754','1610612755',"
                "'1610612756','1610612757','1610612758','1610612759','1610612760','1610612761','1610612762',"
                "'1610612763','1610612764','1610612765','1610612766'}\n")
        f.write("@attribute total_players_accounted NUMERIC\n")
        f.write("@attribute total_players_accounted NUMERIC\n")
        for key in sorted(self.games.keys()):
            game = self.games[key]
            f.write(str(key) + ", " + str(game).strip("(").strip(")"))
            average_time_played = game[9] / game[12]
            f.write(", " + str(average_time_played) + "\n")



def main():
    patta = PlayerArffToTeamArff("arffs/very_large_box/")
    # patta.write_files("arffs/team_arffs/")
    # patta.write_summary_arff("teams_summary.arff")

if __name__ == '__main__':
    main()
