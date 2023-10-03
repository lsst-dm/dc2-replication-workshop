#! /usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from lsst.daf.butler import Butler
from astropy.io import fits

butler = Butler('/dc2/dc2/')
dataId = {'instrument': 'LSSTCam-imSim',
          'visit': 635810,
          'detector': 1}

run_collection1 = 'u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z'
run_collection2 = 'u/nsedaghat/RegeneratedCalexps_w_2022_20_nobfk/20231002T214649Z'
calexp1 = butler.get('calexp', dataId=dataId, collections=run_collection1)
calexp2 = butler.get('calexp', dataId=dataId, collections=run_collection2)

# Compare the wcs of the two calexps.
wcs1 = calexp1.getWcs()
wcs2 = calexp2.getWcs()
print('wcs1 = ', wcs1, '\n')
print('wcs2 = ', wcs2, '\n')


# Also compare at the fits-header level.
file1 = butler.getURI('calexp', dataId=dataId, collections=run_collection1).geturl()
file2 = butler.getURI('calexp', dataId=dataId, collections=run_collection2).geturl()
header1 = fits.getheader(file1)
header2 = fits.getheader(file2)
for key in header1:
    if header1[key] != header2[key]:
        print(f'{key}: \t {header1[key]} \t vs. \t {header2[key]}')
