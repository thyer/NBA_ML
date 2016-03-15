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
            break

    def process_player_file(self, filename):
        player_file = open(self.directory + filename)
        attribute_number = 0
        for line in player_file:
            if "@attribute" in line.lower() and not self.schema_read:
                self.player_files_schema.append(line.split()[1])
                attribute_number += 1
            elif "@relation" in line.lower() or "@data" in line.lower():
                continue
            else:
                feature_vector = line.split(",")
                assert(len(feature_vector) == len(self.player_files_schema))
                assert(self.player_files_schema[8] == "\'team_id\'")
                games_info = None
                if feature_vector[8] in self.teams_info.keys:
                    games_info = self.teams_info.get(feature_vector[8])
                else:
                    games_info = GamesInfo()

                games_info.add_game_data(feature_vector)


class GamesInfo:
    def __init__(self):
        self.games = []

    def add_game_data(self, info):



def main():
    patta = PlayerArffToTeamArff("arffs/very_large_box/")
    # patta.write_files("arffs/team_arffs/")
    # patta.write_summary_arff("teams_summary.arff")

if __name__ == '__main__':
    main()
