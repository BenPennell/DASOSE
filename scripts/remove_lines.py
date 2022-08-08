objects = [12, 15, 19, 25, 30, 44, 52, 54, 61, 69, 72, 80, 88, 93, 99, 279, 295, 299, 317, 963, 1176, 1184, 1188, 1193, 1196, 1205, 1202, 1250, 1342, 1343, 1349, 1350, 1355, 1356, 1357, 1358]

inPath = "A2390SE_dat.txt"
outPath = "A2390SE_dat_trim.txt"

infile = open(inPath, 'r')
lines = infile.readlines()
infile.close()

outfile = open(outPath, 'w')

for i, line in enumerate(lines):
    if i == 0:
        outfile.write(line)
    else:
        splitline = line.split(" ")
        name = splitline[0]
        name = int(name)
        if name not in objects:
            outfile.write(line)
