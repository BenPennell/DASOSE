import astropy.io.fits as fits

field = "A2465C"
hdul = fits.open('E:\AstroResearch\SITELLE\{}\{}\{}_cube_lpf.fits'.format(field, field, field), mode='readonly', menmap=True)
header = hdul[0].header
data = hdul[0].data
hdul.close()

print(data.shape)