import sys
import os

def main():

    files = os.listdir("arffs/very_large_box/")
    for f in files:
        output_file = "arffs/very_large_box_cleaned/" + f.split('.')[0] + ".arff"
        editarff("arffs/very_large_box/" + f, output_file, f.split('.')[0])

def editarff(filename, output_file, name):
    print ("Calling editarff on " + name)
    arff = open(output_file, 'w+')
    arff.write("@relation " + name + "\n")
    arff.write("@attribute box_fg3p Numeric\n")
    arff.write("@attribute box_fgp Numeric\n")
    arff.write("@attribute box_ftp Numeric\n")
    arff.write("@attribute box_minutes Numeric\n")
    arff.write("@attribute box_oreb Numeric\n")
    arff.write("@attribute box_pts Numeric\n")

    with open(filename, 'r') as raw_arff:
        f_data = False
        for line in raw_arff:
            if not f_data:
                if '@data' in line:
                    arff.write(line)
                    f_data = True
            else:
                stats = line.split(',')
                fg3p = str(0)
                fgp = str(0)
                ftp = str(0)
                if(int(stats[0])>0):
                    fg3p = str(int(stats[1]) / int(stats[0]))
                if(int(stats[2])>0):
                    fgp = str(int(stats[3]) / int(stats[2]))
                if(int(stats[4])>0):
                    ftp = str(int(stats[5]) / int(stats[4]))
                seconds_played = str(int(stats[6]))
                oreb = str(int(stats[9]))
                box_pts = str(int(stats[15]))
                arff.write(fg3p + "," + fgp + "," + ftp + "," + seconds_played + "," + oreb + "," + box_pts + "\n")

if __name__ == '__main__':
    main()