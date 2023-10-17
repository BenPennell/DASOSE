import numpy as np
import pipeline as p
import os
from datetime import datetime

cubes_dir = "/home/ben.pennell/SITELLE/cubes/output"
gcat_dir = "/home/ben.pennell/dev/GalaxyCAT"
cubes_names = os.listdir(cubes_dir) # there are 12 datacubes as of 2023.10.08
print(cubes_names)

# needed files, with empty gaps for the name of the cubes to be inserted into.
lpf_path = cubes_dir + "/{}/{}_cube_lpf.fits"
segm_path = gcat_dir + "/segm_maps/{}_segm_MMA_lpf.fits"
elg_list_path = gcat_dir + "/ELG_Lists/{}_ELG_list.txt"

REDSHIFTS = [0.2323, 0.2257, 0.228, 0.228, 0.228, 0.245, 0.245, 0.245, 0.2336, 0.2336, 0.2336, 0.2261] # hardcoded, yes

for i, name in enumerate(cubes_names):
    drawer = p.ELG_Drawer(name, lpf_path.format(name, name), elg_list_path=elg_list_path.format(name), segm=segm_path.format(name, name), redshift=REDSHIFTS[i], z_column=8, med_flux_col=9)
    drawer.elg_brightness_catalogue(algorithm='sum')