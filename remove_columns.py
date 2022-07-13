PATH = "A2390NW_ELG_list.txt"
COUNT = 3

infile = open(PATH, "r")
lines = infile.readlines()
infile.close()

outfile = open(PATH, "w")

for line in lines:
    line = line.split(" ")
    line = line[:-COUNT]
    outline = ""
    for word in line:
        outline += word + " "
    outline+= "\n"
    outfile.write(outline)
    