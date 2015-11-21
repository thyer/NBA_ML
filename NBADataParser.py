import sys
import json

def main():

    if len(sys.argv) < 3:

        print('ARG 1: Comma separated feature list - EX: a:Continuous,b:{ y, n }')
        print('ARG 2: Input JSON filename')
        print('ARG 3: Output filename')
        return

    featuresAndTypes = sys.argv[1].split(";")
    print(featuresAndTypes)
    write_arff(featuresAndTypes, sys.argv[2], sys.argv[3])


def write_arff(featuresAndTypes, filename, outputfile):

    arff = open(outputfile, 'w+')
    arff.write('@relation ' + filename.split('.')[0] + '\n')

    all_teams = set()
    features = []
    for ft in range(0, len(featuresAndTypes)):
        featAndType = str(featuresAndTypes[ft])
        pieces = featAndType.split(':')
        feat = pieces[0]
        type = pieces[1]
        print(type)

        if type == 'Continuous':
            arff.write("@attribute %s %s" % (feat,type) + '\n')
        else:
            arff.write("@attribute \'%s\' %s" % (feat,type) + '\n')

        features.append(feat)

    arff.write("@data")
    jsonstr = ''
    with open(filename, 'r') as jsonfile:
        jsonstr = jsonfile.read()

    games = json.loads(jsonstr)
    for game in games:
        for i in range(0, len(features)):
            arff.write(str(game[features[i]]))
            if i < len(features) - 1:
                arff.write(',')
        arff.write('\n')
        if game['opponent_id'] not in all_teams:
            all_teams.add(game['opponent_id'])
    all_teams_string = ''
    for team in all_teams:
        all_teams_string += '\'' + str(team) + '\'' + ', '
    all_teams_string = all_teams_string[:-2]
    print(all_teams_string)

    arff.close()
    return


if __name__ == '__main__':
    main()