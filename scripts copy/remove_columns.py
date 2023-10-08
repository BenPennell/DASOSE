PATH = "E:\Summer Project 2022\ELG_Lists\A2390C_ELG_list.txt"
COUNT = 1

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
    outline = outline[:-1]
    outline+= "\n"
    outfile.write(outline)
    