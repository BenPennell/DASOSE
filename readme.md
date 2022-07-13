# SITELLE ELG DRAWER
Written by Ben Pennell.

SURP. University of Toronto. July 13th, 2022
__________________________________

# Mutable Constants and Variables
## Line Width Constants
HA_WIDTH = 1 > Thickness of the Hα line
LINE_WIDTH = 2 > Thickness of the NII lines
EDGE_WIDTH = 2 > Edge values to ignore
Each of these are measured in **nanometers**. They represent the width, in nm, of the given line.
Their purpose is to determine what is and isn't part of the emission lines and continuum.
Changing the values will change the output wavenumber arrays created by the emission_range and continuum_range functions

## SIZE
Size is defaulted to 30. Size represents the size of the output images and stacks, and is **half** the width (and height) of the images, in **pixels**
The Size **Must** be consistent for all your images and stacks, since it is relied on for calculations and indexing arrays.

## APERTURE_SIZE
Aperture_Size represents the maximum size of the apertures used for curves of growth. This is defualted to SIZE. Changing this will affect the affect the quality of the curves.
I wouldn't reccomend going lower than SIZE * (0.6) and I also reccomend keeping it in terms of the SIZE.

## CURVE_CLOSENESS
This is the constant used for determining the full light radius in the curves of growth. It is defaulted to 0.05, which means that values within 5% of each other will be defined as 'flat'
I would reccomend changing it based on the bumpyness of your sample, but don't shrink it too much, since these curves don't get too flat.

## INNER_RADIUS and OUTER_RADIUS
These two variables are used to create the average sky value. They are defaulted to 0.75 * SIZE and 0.9 * SIZE. They are these values so they can ignore the contribution from the galaxy. is used in determine_sky_value()

# Miscellaneous Functions
These functions are general and don't need the ELG_Drawer class to be initialized

## def wavenumber(wavelength)
Given a wavelength **In nm**, will return the wavenumber in **cm^-1**

## def wavelength(wavenumber)
Given a wavenumber **cm^-1**, will return the wavelength in **In nm**

## def calculate_wavelength(redshift)
Takes in a redshift and returns wavelength of Ha and NII lines.
This function uses the simple formula λ<sub>obs</sub> = λ<sub>em</sub> * (1 + z) to calculate the observed wavelength of the varius emission lines

    Parameters: 
        redshift (float) ~0.23

    Returns: 
        Ha, NII lower, NII upper (float)

## def mode_of_wonky_array(wonky_array)
Takes in a 3 dimensional array and returns a 2 dimensional array where each entry is the mode of the 3rd axis of the input array
This function is a product of my strange combinations of python lists and numpy arrays. This function takes the mode along the third axis of a 3D array, where that array is a 2 dimensional numpy array, with a python list at each point. This is hardly used, and I am working on removing it entirely for better code. Don't even try to understand it.

    Parameters:
        wonky_array: (3D array of floats)

    Returns:
        values: (2D array of floats)

## def import_fits(self, path)
Loads in a .fits cutout as a 2D array

    Parameters:
        path: (String) path to file
    
    Returns:
        data: (3D array of floats) 2D array that represents an image
    
# ELG_Drawer Class
## def __init _(self, name, cube_path, elg_list_path="None", segm="None", redshift=0, z_column=7):
Class for creating images of ELGs from .fits files and stacking those images. Every function below this is a part of this class and needs the class initialized to work

        Parameters:
            name: (String) name of the object. Example: "A2390C" or "A2465NE"
            cube_path: (String) path to the .fits datacube

            elg_list_path: (String) path to the elg list generated by Find_emission_candidate. Optional, defaults to "None"
            segm: (String) path to the segmentation map. Effectively - the image with cutouts for each ELG. Defaults to "None"
            redshift: (float) redshift to the galaxy cluster. Defaults to 0
            z_column: (int) the index of the column that contains the redshifts in the elg_list. Defaults to 7

## elg_list
The elg_list is an important part of the process. Technically, it is optional, but is highly encouraged.
The elg list is the list generated by Qing Liu's SITELLE_elg_finder. It has the following form:

    NUMBER xcentroid ycentroid ellipticity orientation equivalent_radius flag type redshift med_flux
    13 351.34 33.71 0.08 48.73 4.15 1 0 0.234 0.021192390471696854
    24 1895.17 48.77 0.22 -70.87 5.94 1 0 0.221 0.04878013953566551
    33 1005.6 58.84 0.28 15.66 1.87 1 0 0.233 0.005213028751313686
    38 1248.84 70.17 0.58 21.12 1.95 1 0 0.230 0.0017722846241667867
    65 1742.58 119.59 0.32 -51.69 4.41 1 0 0.229 0.01961141638457775
    83 868.0 153.37 0.39 76.07 3.34 1 0 0.228 0.0039884550496935844
    85 1326.62 151.16 0.53 -53.13 1.6 1 0 0.250 0.004018770530819893
    98 1387.69 184.42 0.22 7.29 2.11 2 0 0.238 0.009183024056255817
    100 199.18 188.41 0.58 -81.15 2.03 2 0 0.230 -0.0016234238864853978
    102 1791.9 195.56 0.64 -36.93 2.46 2 0 0.230 0.012860113754868507

What is important to understand about this list is the following:
    - The 'type' flag is represented by 0, 1 or 2, for the type of ELG. It is not used in this program, but would be nice to have. the 'type' flag is not generated by Qing's code, and has to be manually insterted
    - The redshift is likewise not generated by Qing's code. It must also be inserted
    - I created a script for adding these called append_redshift.py
    - Based on your elg_list, the indeces may be mixed up. What is crucial is that it starts with the name/number of the ELG, then xCentroid and then yCentroid. The redshift can be put anywhere, and the z_column argument in def __init _() can be used. Frequently I have to use 7 or 8 as the column. If your code flies through the hα images super fast and they end up blank, this was likely your problem.

## the write file
As part of this class, I created a log file (log.txt) which can be found in the output folder. It documents what was going on with this specific analysis, and is useful for not losing track of what you're doing. Lot's of important information is stored there.
You can use the write_file() method to write more into the file, or write in it manually. I **highly reccomend** that you do this. If you're running multiple analyses of a specific cube, it will be easy to lose track of what you've done.

## def change_outPath(self, outPath)
Changes the outPath for the datacube, in case you want to use the same cube to create multiple different kinds of stacks.

        Parameters:
        outPath: (String) The name of the folder to be created from the current working directory

# Creating Images
## def generate_images(self, image_types, algorithm='sum', elg_list_path=None)
This is the runner function that creates all the images. This is the function you should call to make images normally. The process will be underlines below.

    Parameters:
        image_types: (list of floats) list of all the image types that will be generated. The following options: 'continuum', 'halpha', 'nIIl' and 'nIIu'
        algorithm: (Optional) (String) algorithm type to use. Default is sum, there may not be other options.
        elg_list_path: (Optional) (String) path to elg_list if cube was not initialized with one
    
## Example Code for creating images

```
import pipeline as p

CUBE_PATH = 'E:/SITELLE/A2390SE/output/A2390SE_cube.fits'
SEGM_PATH = 'E:/SITELLE/A2390SE/output/A2390SE_segm_MMA_lpf.fits'
ELG_LIST_PATH = 'A2390SE_ELG_list.txt'

NAME = 'A2390SE'
REDSHIFT = 0.228

cube = p.ELG_Drawer(NAME, CUBE_PATH, elg_list_path=LIST_PATH, segm=SEGM_PATH, redshift=REDSHIFT, z_column=8)

cube.write_file("I am creating images of the Southeast flanking field for A2390 to see how it compares to the center field. This time I have removed the bad detections, so only the good images will be created")

cube.generate_images(['continuum', 'halpha'], algorithm='sum')
```
This will generate continuum and hα images for all the ELGs found in the elg list. Let's break the code down line by line to appreciate it.

First, we import the pipeline (I prefer to import as p than to import all). Then, we establish where the cube, segmentation map and elg_list can be found. Then, we add the requisite information about the cluster. The name, and the redshift. 

We then initialize the ELG_Drawer. The next step is to actually generate the images. We have to use a list to tell the program which images we want. Each type will be saved in its own folder. Finally, we include how we want the images created.

The images are created by combining multiple channels together, and in general, we want to sum them. You can also combine them by mean, median or mode; it's up to you.

Now, here are all the methods in this category



# Creating Stacks

# Creating Curves of Growth