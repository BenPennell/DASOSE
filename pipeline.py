import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
import os

from astropy.visualization import (MinMaxInterval,PercentileInterval, SqrtStretch,HistEqStretch,ImageNormalize,SquaredStretch,AsymmetricPercentileInterval, AsinhStretch)

# Wavelengths
HALPHA_WAVELENGTH = 656.3 #nm
NII_LOWER_WAVELENGTH = 654.8 #nm
NII_UPPER_WAVELENGTH = 658.3 #nm

# Line Width Constants
HA_WIDTH = 2
NII_WIDTH = 2
EDGE_WIDTH = 2

SIZE = 20

'''
No Datacubes needed
----------------------
'''

def wavenumber(wavelength):
    '''Given wavelength in nm, will return wavenumber in 1/cm

    Parameters: 
        wavelength in nm, float

    Returns: 
        wavenumber in 1/cm, float
    '''
    return (1e7)/wavelength

def wavelength(wavenumber):
    '''Given wavenumber in 1/cm, will return wavelength in nm

    Parameters: 
        wavenumber in 1/cm, float

    Returns: 
        wavelength in nm, float
    '''
    return (1e7)/wavenumber

def calculate_wavelength(redshift):
    '''Takes in a redshift and returns wavelength of Ha and NII lines.

    Parameters: 
        redshift (float) ~0.23

    Returns: 
        Ha, NII lower, NII upper (float)
    '''

    ha_shifted = HALPHA_WAVELENGTH * (1 + redshift)
    nIIL_shifted = NII_LOWER_WAVELENGTH * (1 + redshift)
    nIIU_shifted = NII_UPPER_WAVELENGTH * (1 + redshift)

    return ha_shifted, nIIL_shifted, nIIU_shifted

'''
Image Generator
---------------
'''
class ELG_Drawer:

    def __init__(self, name, path, segm="None", outPath="output"):
        '''Class for creating images of ELGs from .fits files and stacking those images

        Parameters:
            name: (String) name of the object
            path: (String) path to the .fits datacube
            segm: (String) path to the segm datacube. Effectively - the datacube with cutouts for each ELG. Defaults to none
            outPath: (String) path for where the objects should be saved. Defaults to /output in the present working directory
        '''
        self.name = name

        hdul = fits.open(path, mode='readonly', memmap=False)
        self.header = hdul[0].header
        self.data = hdul[0].data
        hdul.close()

        # Set the segm path and open it. I'm allowing users to not have a segm, so it will simply not load one in if none is given
        self.segmh = ""
        self.segm = segm
        try:
            hdul = fits.open(segm, mode='readonly', memmap=False)
            self.segmh = hdul[0].header
            self.segm = hdul[0].data
        except:
            print("No segm file given, will proceed without one. This may throw errors later")   
        
        self.outPath = "./" + outPath
        
        try:
            os.mkdir("./{}".format(outPath))
            os.mkdir("./{}/pic".format(outPath))
            os.mkdir("./{}/fits".format(outPath))
        except:
            print("Directory ./{} already exists. Exisitng directory will be used".format(outPath))

        self.textPath = "./" + outPath + "/log.txt"
        f = open(self.textPath, "w")
        f.write("Object: {}\nPath: {}\n".format(self.name, path))
        f.close()
        
    def write_file(self, message):
        '''Writes to the log file a given message

        Parameters:
            message: (String) message to write
        '''

        outFile = open(self.textPath, "a")
        outFile.write(message + "\n")
        outFile.close()

    def get_max_wavenumber(self):
        '''Likely useless function that determines the upper boundary of the datacube in wavenumbers
        
        Returns:
            wavenumber: (float) maximum wavenumber in 1/cm
        '''

        min_wavenumber = self.header['CRVAL3']
        wavenumber_step = self.header['CDELT3']
        step_count = self.header['NAXIS3']

        max_wavenumber = min_wavenumber+(step_count-1)*wavenumber_step

        return max_wavenumber

    def get_wavenumber_array(self):
        '''Returns an array which contains the wavenumber for each channel
        
        Returns:
            wavn_array: (float) array of wavenumbers
        '''

        min_wavenumber = self.header['CRVAL3']
        max_wavenumber = self.get_max_wavenumber()
        wavenumber_step = self.header['CDELT3']
        
        wavn_array = np.arange(min_wavenumber, max_wavenumber, wavenumber_step)

        return wavn_array

    def get_channel(self, wavenumber):
        '''Determines which channel a given measured wavenumber emission line lies

        Parameters: 
            wavenumber: (float) wavenumber in 1/cm 
        
        Returns: 
            channel: (int) nearest channel to the given wavenumber
        '''

        wavenumber_array = self.get_wavenumber_array()

        channel = np.argmin(np.abs(wavenumber - wavenumber_array))

        return channel

    def continuum_range(self, redshift):
        '''Determins the range in which the continuum of the stellar portion of the galaxy is measured

            Takes in a redshift of a Galaxy, and considering line widths and edge of the detection range it determines the range of the continuum

            The continuum is defined as being (from Qing's paper):
                -2 nm from the edge of measurement (EDGE_WIDTH)
                -1.5 * (1 + z) nm away from NII lines (NII_WIDTH)

        Parameters:
            redshift: (float) redshift of galaxy ~0.23
        
        Returns:
            range: (array of floats) wavenumbers that represent the channels of the Emission
        '''

        # Determine expected wavenumbers of redshifted lines
        _, nl_wl, nu_wl = calculate_wavelength(redshift) 

        # Determine boundaries of nII lines
        # We do this by taking lowest nL and highest nU border
        nII_boundary = (wavenumber(nl_wl - (NII_WIDTH * (1 + redshift))), wavenumber(nu_wl + (NII_WIDTH * (1 + redshift))))

        # Determine boundary of the measurement itself in wavenumbers
        wavn_array = self.get_wavenumber_array()

        m_boundary = (wavenumber(wavelength(np.min(wavn_array)) - EDGE_WIDTH), wavenumber(wavelength(np.max(wavn_array)) + EDGE_WIDTH))

        # What we have now computed is the range that the continuum does not cover
        # We will simply compare each channel to each range to see whether it falls in it or not
        # Surely this could be more efficient
        continuum_wavn_array = []
        for i in range(len(wavn_array)):
            # First, check if it is within range of measurement boundaries
            if wavn_array[i] > m_boundary[0] and wavn_array[i] < m_boundary[1]:
                # Next, check if it is not in range of the lines
                if wavn_array[i] > nII_boundary[0] or wavn_array[i] < nII_boundary[1]: # ha
                            continuum_wavn_array.append(wavn_array[i]) 
        
        return continuum_wavn_array

    def emission_range(self, redshift):
        '''Determins the range in which the emission line of the galaxy is measured

            The width of the emission line is defined as (from Qing's paper):
                -0.5 * (1 + z) nm from emission line. (HA_WIDTH)

        Parameters:
            redshift: (float) redshift of galaxy ~0.23
        
        Returns:
            range: (array of floats) wavenumbers that represent the channels of the Emission
        '''

        ha_wl, _, _ = calculate_wavelength(redshift) 

        ha_boundary = (wavenumber(ha_wl - (HA_WIDTH * (1 + redshift))), wavenumber(ha_wl + (HA_WIDTH * (1 + redshift))))

        wavn_array = self.get_wavenumber_array()

        emission_wavn_array = []
        for i in range(len(wavn_array)):
            if wavn_array[i] < ha_boundary[0] and wavn_array[i] > ha_boundary[1]:
                emission_wavn_array.append(wavn_array[i]) 
        
        return emission_wavn_array

    def sum_channels(self, wavn_array, xLoc, yLoc, algorithm="mean", name=""):
        ''' Adds all channels corresponding to a certain wavenumber array together to create images

        Parameters:
            wavn_array: (array) wavenumbers each corresponding to a channel, that will be included in the image
            xLoc: (float) x location that we want to get the measurements from
            yLoc: (float) y location that we want to get the measurements from

            algorithm: (String) the algorithm to use to create the images. default='mean'. Options: 'mean', 'sum', 'median'
            name: (String) used only if a segm fits file is used for better images

        Returns:
            output: (float) Represents the average of all measurements, to be used in the image
        '''

        measurements = []
        for wavn in wavn_array:
            channel = self.get_channel(wavn)
            value = self.data[channel, yLoc, xLoc]
            if not np.isnan(value):
                if name != "":
                    if self.segm[yLoc, xLoc] == name or self.segm[yLoc, xLoc] == 0:
                        measurements.append(value)
                    else:
                        measurements.append(0)
                else:
                    measurements.append(value)
        
        output = []
        if(algorithm == "mean"):
            output = np.average(measurements)
        elif(algorithm == 'sum'):
            output = np.sum(measurements)
        elif(algorithm == 'median'):
            output = np.median(measurements)
        else:
            raise ValueError("Invalid algorithm specified. The choices are: 'mean', ")      
        
        return output
    
    def create_image(self, wavn_image, xCentroid, yCentroid, algorithm="mean", name=""):
        '''Generates an image around a certain point

        Parameters:
            wavn_array: (array of floats) each wavenumber represents a channel in the cube that will be summed for the image
            xCentroid: (float) x location of the center of the image
            yCentroid: (float) y location of the center of the image


            algorithm: (String) the algorithm to use to create the images. default='mean'. Options: 'mean', 'sum', 'median'
            name: (String) used only if a segm fits file is used for better images

        Returns:
            image: (2D array of floats) each point in the array represents a pixel in the image
        '''
        #write to the outFile for organization purposes
        self.write_file("Channel stacking algorithm: {}".format(algorithm))

        xCentroid = int(xCentroid)
        yCentroid = int(yCentroid)
        xValues = np.arange(xCentroid - SIZE, xCentroid + SIZE, 1)
        yValues = np.arange(yCentroid - SIZE, yCentroid + SIZE, 1)
        image = np.zeros((2 * SIZE, 2 * SIZE))

        for i, xLoc in enumerate(xValues):
            for j, yLoc in enumerate(yValues):
                image[i][j] = self.sum_channels(wavn_image, xLoc, yLoc, algorithm, name=name)
                
        return image

    def save_pdf(self, name, image, stack=False):
        '''creates a pdf using matplotlib's imshow() function

        Parameters:
            name: (string) name for file to be saved as
            image: (array of floats) 2 dimensional numpy array each containing a float representing colour make use of self.create_image

            stack: (boolean) whether it is a stack or not. This gives it a special directory. defaults to False

        Returns:
            None. The pdf will be automatically saved.
        '''
        picsPath = self.outPath
        fitsPath = self.outPath
        if stack == False:
            picsPath += "/pic"
            fitsPath += "/fits"

        try:
            norm = ImageNormalize(data=image, stretch=AsinhStretch())

            plt.imshow(image, origin="lower", norm=norm)
            plt.savefig("{}/{}.png".format(picsPath, name))
            fits.writeto("{}/{}".format(fitsPath, name), image, overwrite=True)
        except:
            print("There was an error saving image {}".format(name))
            print("In case there was a data issue, I will print it so you can check if something is wrong: {}".format(image))
    
    def import_image(self, path):
        '''Loads in a .fits cutout as a 2D array

        Parameters:
            path: (String) path to file
        
        Returns:
            data: (3D array of floats) 2D array that represents an image
        '''

        hdul = fits.open(path, mode='readonly', memmap=False)
        data = hdul[0].data
        hdul.close()

        return data

    def load_images(self):
        '''Loads in all .fits cutouts from the output directory into a 3D array
        
        Returns:
            images: (3D array of floats) 3D array of images
        '''
        path = self.outPath + "/fits"

        images = np.zeros((len(os.listdir(path)), 2 * SIZE, 2 * SIZE))
        print('Created images: {}'.format(images))

        for i, filename in enumerate(os.listdir(path)):
            image = self.import_image(os.path.join(path, filename))
            try:
                images[i] = image
                print('loaded in image {}'.format(i))
            except:
                i -= 1

        return images

    def create_stack(self, algorithm="mean"):
        '''Stacks a series of images created by the create_image function

        Parameters:
            algorithm: (String) the algorithm to use to create the images. default='mean'. Options: 'mean', 'sum', 'median'

        Returns:
            image: (2D array of floats) each point in the array represents a pixel in the image
        
        Exceptions:
            Will complain if you don't provide a valid algorithm
        '''
        #write to the outFile for organization purposes
        self.write_file("Image stacking algorithm: {}".format(algorithm))

        images = self.load_images()

        image = np.zeros((0,0))

        if algorithm == "mean":
            image = images.mean(axis=0)
        elif algorithm == 'sum':
            image = images.sum(axis=0)
        elif algorithm == 'median':
            image = np.median(images, axis=0)
        else:            
        # If no valid algorithm type was specified
            raise ValueError("Invalid algorithm specified. The choices are: 'mean', 'sum', 'median'")     

        return image