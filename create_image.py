import numpy as np
import pipeline as p

CUBE_PATH = 'E:/SITELLE/A2390/C4_Halpha/output/A2390C_cube.fits'
SEGM_PATH = 'E:/SITELLE/A2390/C4_Halpha/output/A2390C_segm_MMA_lpf.fits'

A2390 = p.ELG_Drawer("A2390", CUBE_PATH, outPath="A2390_continuum", segm=SEGM_PATH)
A2390.write_file("Testing with new edge widths. It wasn't working before")
elg_list = np.loadtxt("A2390C_ELG_list.txt", skiprows=1)
# name: line[0]
# xCentroid: line[1]
# yCentroid: line[2]
# redshift: line[7]
# type: line[8]

# for elg in elg_list:
#     name = int(elg[0])
#     print("Printing ELG {}...".format(name))
#     range = A2390.continuum_range(elg[7])
#     image = A2390.create_image(range, elg[1], elg[2], algorithm="sum", name=name)
#     A2390.save_pdf(name, image)

image = A2390.create_stack(algorithm='median')
A2390.save_pdf("stack", image, stack=True)