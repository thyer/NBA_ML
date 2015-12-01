import sys
import requests
import json

def main():

    if len(sys.argv) < 2:

        print('ARG 1: NBA Stats api key')
        return

    apikey = sys.argv[1]
    download_player_stats(apikey)

    return


def download_player_stats(apikey):

    test = "https://probasketballapi.com/players?api_key=" + apikey
    r = requests.post(test)
    players = r.text
    playersjson = json.loads(players)
    for player in playersjson:
        name = player["player_name"].replace(" ", "_")
        id = player["player_id"]
        stats_url = "https://probasketballapi.com/stats/players?" + 'api_key=' + apikey + "&player_id=" + str(id)
        print(stats_url)
        r = requests.post(stats_url)
        data = open("raw_data/" + name + ".json", 'w+')
        data.write(r.text)
        data.close()

if __name__ == '__main__':
    main()