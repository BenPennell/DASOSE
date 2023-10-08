import astropy.io.fits as fits

fitscube=fits.open('E:/SITELLE/A2465/2345354p.fits')
hdr = fitscube[0].header
hdr['STEP_NB']=hdr['NAXIS3']
# hdr['HIERARCH CRVAL3']=hdr['AXIS_MIN']
# hdr['HIERARCH CRPIX3']='1.0'
# hdr['HIERARCH CDELT3']=hdr['axis_step']
# hdr['TARGETR']=hdr['target_ra']
# hdr['TARGETD']=hdr['target_dec']
fitscube.writeto('E:/SITELLE/A2465/A2465-2345354.fits', overwrite=True)