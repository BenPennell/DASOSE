PATH = "E:\Summer Project 2022\ELG_Lists\A2390C_ELG_list.txt"
COUNT = 1
POSITION = 6

infile = open(PATH, "r")
lines = infile.readlines()
infile.close()

outfile = open(PATH, "w")

for line in lines:
    line = line.split(" ")
    outline = ""
    for i, word in enumerate(line):
        word = word.strip()
        outline += word + " "
        if i == POSITION:
            for k in range(COUNT):
                outline += "0 "
                
    outline += "\n"
    outfile.write(outline)