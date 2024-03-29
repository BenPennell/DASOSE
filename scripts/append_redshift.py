import pickle
import numpy as np

FIELD = "RXJ2129S"
PATH = 'E:\AstroResearch\Summer Project 2022\ELG_Lists\{}_ELG_list.txt'.format(FIELD)
infile = open("E:\AstroResearch\SITELLE\{}\{}\{}-cc-MMA_lpf.pkl".format(FIELD, FIELD, FIELD), 'rb')

new_dict = pickle.load(infile)
infile.close()

elg_list_full = open(PATH, 'r')
lines = elg_list_full.readlines()

elg_list_full.close()
elg_list_full = open(PATH, 'w')
elg_list_full.write(lines[0])
lines.pop(0)

for line in enumerate(lines):
    line = line[1]
    splitline = line.split()

    name = splitline[0]
    name = str(name)

    line = line[:-1]
    elg_list_full.write(line + " {} {:.3f}\n".format(0, new_dict['Ha-NII_gauss'][name]['z_best']))