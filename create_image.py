import numpy as np
import pipeline as p
import matplotlib.pyplot as plt

NAME = 'A2390C'
CUBE_PATH = 'E:\SITELLE\A2390C\A2390C\A2390C_cube_lpf.fits'
SEGM_PATH = 'E:\SITELLE\A2390C\A2390C\A2390C_segm_MMA_lpf.fits'
LIST_PATH = 'E:\Summer Project 2022\ELG_Lists\A2390C_ELG_list.txt'
REDSHIFT = 0.228

###-------------------------------------------------###
cubes = ['A2390C']
redshift = [0.2336, 0.2336]

for i, field in enumerate(cubes):
     z = redshift[i]
     cube = p.ELG_Drawer(field, 'E:\AstroResearch\SITELLE\{}\{}\{}_cube_lpf.fits'.format(field, field, field), elg_list_path='E:\AstroResearch\Summer Project 2022\ELG_Lists\{}_ELG_list.txt'.format(field), segm='E:\SITELLE\{}\{}\{}_segm_MMA_lpf.fits'.format(field, field, field), redshift=z, z_column=11, med_flux_col=12)
     cube.append_median_flux()
     cube.generate_images(['continuum', 'halpha'], algorithm='sum')
     cube.generate_stacks(['mean', 'sum', 'median'], ['continuum', 'halpha'], percentiles=(10, 90))
     cube.analyze_various_curves(['mean', 'median'], ['continuum', 'halpha'])


#cube = p.ELG_Drawer(NAME, CUBE_PATH, elg_list_path=LIST_PATH, segm=SEGM_PATH, redshift=REDSHIFT, r200=1000, z_column=8, med_flux_col=9)

#elg_list = np.loadtxt(LIST_PATH, skiprows=1)
#cube.write_file("So, this time we are making stacks based on whether or not the object is within R200 (we set it as 1mpc")
#cube.generate_stacks(['mean', 'median'], ['continuum', 'halpha'], percentiles=(10, 90), use_R200=1)
#cube.generate_stacks(['mean', 'median'], ['continuum', 'halpha'], percentiles=(10, 90), use_R200=2)
#cube.write_file("\nNo longer subtracting sky value, using segm_map and removed bad detections (70 objects)")
#cube.append_median_flux()
#cube.generate_images(['continuum', 'halpha'], algorithm='sum')
#cube.generate_stacks(['mean', 'sum', 'median'], ['continuum', 'halpha'], percentiles=(10, 90))
# INTERVAL = 20
# for i in np.arange(0, 100, INTERVAL):
#     cube.generate_stacks(['mean', 'median', 'sum'], ['continuum', 'halpha'], percentiles=(i, i+20), name="Interval ({}, {}) ".format(i, i+20))
#cube.generate_stacks(['mean', 'median', 'sum'], ['continuum', 'halpha'])


#cube.analyze_various_curves(['mean', 'median'], ['continuum', 'halpha'])

def make_some(cube, elg_list):
    for elg in elg_list:

        continuum = cube.continuum_range(elg[7])
        emission = cube.emission_range(elg[7], "halpha")
        cube.graph_wavn(elg[0], continuum, emission, int(elg[1]) + 10, int(elg[2]) + 10)

TYPE = 'emission'
IMTYPE = 'mean'
# sttype = 'median' 
sttypes = ['mean', 'median', 'sum'] #'mode', 'sum']

def compare():
    A2390 = p.ELG_Drawer("Comparing stacks".format(TYPE, IMTYPE, 'mean'), CUBE_PATH, segm=SEGM_PATH)

    image_1 = A2390.import_fits("./output/poachable_pictures_continuum/Stack of A2390 ELG continuum, stacked by median")
    image_2 = A2390.import_fits("./output/poachable_pictures_emission/Stack of A2390 ELG emission, stacked by median")

    image = A2390.compare(image_1, image_2)
    A2390.save_pdf("mean stack comparison. continuum is 0 emission is 1", image, stack=True)

def create_curves(cube):
    for sttype in sttypes:
        #continuum = cube.import_fits("./output/poachable_pictures_emission/Stack of A2390 ELG emission, stacked by {}".format(sttype))
        emission = cube.import_fits("./output/poachable_pictures_emission/Stack of A2390 ELG emission, stacked by {}.fits".format(sttype))

        #cont = cube.curve_of_growth("Curve of growth continuum stacked by {}".format(sttype), continuum)
        emi = cube.curve_of_growth("Curve of growth emission stacked by {}".format(sttype), emission)

        #cube.compare_curves("Curve of growth comparisons for {} stacks".format(sttype), cont, emi)

def generate_images(cube, elg_list, algorithm='mean'):
    '''
    '''
    cube.write_file("Image algorithm type: {}".format(algorithm))
    for elg in elg_list:
        name = int(elg[0])
        print("Printing ELG {}...".format(name))
        continuum_range = cube.continuum_range(elg[7])

        image = cube.create_image(continuum_range, elg[1], elg[2], algorithm=algorithm, name=name) # emission=True, redshift=elg[7])
        cube.save_pdf("A2390 Object {} {}".format(name, TYPE), image, elg[1], elg[2])

def generate_stack(cube, name, algorithm='mean'):
    '''
    '''
    cube.write_file("Stack algorithm type: {}, saved as {}".format(algorithm, name))
    image = cube.create_stack(algorithm=algorithm, percentiles=(0, 100))
    cube.save_pdf(name, image, stack=True)
    cube.curve_of_growth(image, name=name)

def buncha_types(cube):
    for sttype in sttypes:
        cube.write_file("Testing version of the stack: {}, {}".format(IMTYPE, sttype))

        generate_stack(cube, "Stack of all A2390NW objects stacked by {}".format(sttype), algorithm=sttype)

def in_range(value):
    if value > 2000:
        return False
    elif value < 30:
        return False
    
    return True

def run_all_objects(elg_list):
    for elg in elg_list:
        elg_name = int(elg[0])
        x_location = float(elg[1])
        y_location = float(elg[2])

        if in_range(x_location) and in_range(y_location):
            range = cube.get_wavenumber_array()

            image = cube.create_image(range, x_location, y_location, algorithm="sum", name=elg_name)

            cube.save_pdf("A2390SE Object #{}".format(elg_name), image, x_location, y_location, stack=False)

def create_curve_data():
    cubes = ['A1736C', 'A2219C', 'A2390C', 'A2390NW', 'A2390SE', 'A2465C', 'A2465NE', 'A2465SW', 'RXJ2129', 'ZWCL0823']
    redshift = [0.2323, 0.2257, 0.228, 0.228, 0.228, 0.245, 0.245, 0.245, 0.2336, 0.2261]
    flanking = [0, 0, 0, 1, 1, 0, 1, 1, 0, 0]

    buckets = [(10,90), (10,30), (30, 50), (50, 70), (70, 90)] #(50, 60), (60, 70), (70, 80), (80, 90)]
    stackType = "mean"

    out_path = "./curve_data_short.txt"
    out_file = open(out_path, 'w')
    out_file.write("Name flanking? redshift 1090 1030 3050 5060 6070 7080 8090\n")

    for i, field in enumerate(cubes):
        z = redshift[i]
        f = flanking[i]
        cube = p.ELG_Drawer(field, 'E:\SITELLE\{}\{}\{}_cube_lpf.fits'.format(field, field, field), elg_list_path='E:\Summer Project 2022\ELG_Lists\{}_ELG_list.txt'.format(field), segm='E:\SITELLE\{}\{}\{}_segm_MMA_lpf.fits'.format(field, field, field), redshift=z, z_column=8, med_flux_col=9)
        
        outf = "yes"
        if f == 0:
            outf = "no"

        output = "{} {} {}".format(field, outf, z)

        for bucket in buckets:
            image = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'continuum'), percentiles=bucket)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            continuum = curve[3]

            image = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'halpha'), percentiles=bucket)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            emission = curve[3]

            value = emission / continuum

            output += " {:.3f}".format(value)
        
        out_file.write(output + "\n")

def create_weighted_plot():
    cubes = ['A1736C', 'A2219C', 'A2390C', 'A2390NW', 'A2390SE', 'A2465C', 'A2465SW', 'RXJ2129', 'ZWCL0823']
    redshift = [0.2323, 0.2257, 0.228, 0.228, 0.228, 0.245, 0.245, 0.2336, 0.2261]

    buckets = [(10,90), (10,30), (30, 50), (50, 70), (70, 90)] #(50, 60), (60, 70), (70, 80), (80, 90)]
    stackType = "mean"
    xVals = np.array([0, 1, 2, 3, 4])
    yVals = []

    for bucket in buckets:
        values = []
        lengths = []
        for i, field in enumerate(cubes):
            z = redshift[i]
            cube = p.ELG_Drawer(field, 'E:\SITELLE\{}\{}\{}_cube_lpf.fits'.format(field, field, field), elg_list_path='E:\Summer Project 2022\ELG_Lists\{}_ELG_list.txt'.format(field), segm='E:\SITELLE\{}\{}\{}_segm_MMA_lpf.fits'.format(field, field, field), redshift=z, z_column=8, med_flux_col=9)
            
            image, length = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'continuum'), percentiles=bucket, return_length=True)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            continuum = curve[3]
            lengths.append(length)

            image = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'halpha'), percentiles=bucket)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            emission = curve[3]

            value = emission / continuum

            values.append(value)

        total_value = 0

        for i, value in enumerate(values):
            total_value += lengths[i] * value / np.sum(lengths)
            #print(np.sum(lengths))
    
        yVals.append(total_value)

    print(yVals)
    return
    plt.plot(xVals[1:], yVals[1:], "o", color="black", markersize=15)
    plt.plot(xVals[0], yVals[0], "o", color="red", markersize=15)
    plt.axhline(y=1, color="black")
    plt.axvline(x=0.5, color="black", linewidth="0.5")
    plt.axvline(x=1.5, color="black", linewidth="0.5")
    plt.axvline(x=2.5, color="black", linewidth="0.5")
    plt.axvline(x=3.5, color="black", linewidth="0.5")
    plt.xticks(xVals, ['All Galaxies', '(10,30)', '(30, 50)', '(50, 70)', '(70, 90)'])
    plt.title("Ratio of emission to continuum half light radii for cluster galaxies", fontsize=20)
    plt.xlabel("Continuum Flux Percentile of ELGs", fontsize=20)
    plt.ylabel("$r_{emission}/r_{continuum}$", fontsize=25)
    plt.show()
    plt.clf()

def R200_plot():
    cubes = ['A1736C', 'A2219C', 'A2390C', 'A2390NW', 'A2390SE', 'A2465C', 'A2465SW', 'A2465NE', 'RXJ2129', 'ZWCL0823']
    field_type = [1, 1, 1, 0, 0, 1, 0, 0, 1, 1]
    redshift = [0.2323, 0.2257, 0.228, 0.228, 0.228, 0.245, 0.245, 0.245, 0.2336, 0.2261]
    stackType = "mean"
    params = {'mathtext.default': 'regular' } 

    colors = ['orange', 'green', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'brown', 'black']
    shape = ['o', 'o', 'o', 's', '^', 'o', 's', '^', 'o', 'o']

    for k, field in enumerate(cubes): 
        arraything = [1, 1.2]
        max = len(cubes)
        offset = 0.08
        true_offset = offset * (k - (max / 2)) / max
        
        z = redshift[k]

        R200 = 1000
        if field_type[k] == 0:
            R200 = 0
        cube = p.ELG_Drawer(field, 'E:\SITELLE\{}\{}\{}_cube_lpf.fits'.format(field, field, field), elg_list_path='E:\Summer Project 2022\ELG_Lists\{}_ELG_list.txt'.format(field), segm='E:\SITELLE\{}\{}\{}_segm_MMA_lpf.fits'.format(field, field, field), r200=R200, redshift=z, z_column=8, med_flux_col=9)
        
        xValues = []
        values = []

        possible_i = arraything
        if field_type[k] == 0:
            possible_i = []
            possible_i.append(arraything[1])
        
        for i in possible_i:
            image = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'continuum'), percentiles=(10, 90), use_R200=i)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            continuum = curve[3]

            image = cube.create_stack(algorithm=stackType, path="{}/fits/{}".format(cube.outPath,'halpha'), percentiles=(10, 90), use_R200=i)
            curve = cube.curve_of_growth(image, save=False)
            # curve = (xVals, curve, half_light, half_r, full_light, full_r)
            emission = curve[3]

            value = emission / continuum
            values.append(value)
            xValues.append(i + true_offset)
        
        plt.plot(xValues, values, shape[k], color=colors[k], markersize=15, label=field)
    
    plt.axhline(y=1, color="black")
    plt.axvline(x=1.1, color="black", linewidth="0.5")
    plt.xticks(arraything, ['Within 1Mpc', 'Outside 1Mpc'], fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(prop={'size': 14})
    plt.title("Half-light radii ratio based on distance from center of cluster", fontsize=36)
    plt.xlabel("Continuum Flux Percentile of ELGs", fontsize=34)
    plt.ylabel("$r_{emission}/r_{continuum}$", fontsize=34)
    plt.show()
    plt.clf()

def create_plot():
    path = "curve_data_short.txt"
    infile = open(path)
    infile.readline()

    params = {'mathtext.default': 'regular' } 

    data = infile.readlines()
    xVals = np.array([0, 1, 2, 3, 4])
    colors = ['orange', 'green', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'brown', 'purple']
    shape = ['o', 'o', 'o', 's', '^', 'o', 's', '^', 'o', 'o']

    for k, line in enumerate(data):
        line = line.split(" ")
        name = line[0]

        data = line[3:]
        for i, val in enumerate(data):
            data[i] = float(val)
        
        max = len(data)
        offset = 0.2
        true_offset = offset * (k - (max / 2)) / max
        if name != "A2465NE":
            plt.plot(xVals + true_offset, data, shape[k], color=colors[k], markersize=20, label=name)
    
    plt.plot(xVals, [0.9702921734555076, 0.9577845611144407, 0.9533065481842887, 0.9893105162806368, 0.9718773807352569], "*", color="black", markersize=30, label="Weighted Average")
    plt.axhline(y=1, color="black")
    plt.axvline(x=0.5, color="black", linewidth="1")
    plt.axvline(x=1.5, color="black", linewidth="0.5")
    plt.axvline(x=2.5, color="black", linewidth="0.5")
    plt.axvline(x=3.5, color="black", linewidth="0.5")
    plt.xticks(xVals, ['All galaxies', '(10,30)', '(30, 50)', '(50, 70)', '(70, 90)'], fontsize=24)
    plt.yticks(fontsize=30)
    plt.legend(prop={'size': 16})
    plt.title("Ratio of emission to continuum half light radii for cluster galaxies", fontsize=32)
    plt.xlabel("Continuum Flux Percentile of ELGs", fontsize=34)
    plt.ylabel("$r_{emission}/r_{continuum}$", fontsize=34)
    plt.show()
    plt.clf()

#R200_plot()
#create_curve_data()
#create_plot()
#create_weighted_plot()
# run_all_objects()
# buncha_types(cube)

