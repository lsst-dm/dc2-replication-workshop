#! /usr/bin/env python3

'''
A script that locates a butler run collection based on the passed tag name
(e.g. w_2022_19), loads a spcific calexp from the collection (hard coded
data id), compares it to a reference calexp (also hard coded data id), and
displays the difference image.

This was used to locate a weekly build that produces calexps that are
close enough to the backed-up DL0.1.1 dataset.
'''

import sys
import numpy as np
import matplotlib.pyplot as plt
from lsst.daf.butler import Butler
from astropy.io import fits


#tag = sys.argv[1] if __name__ == '__main__' else 'w_2022_05'
tag = 'w_2022_20_nobfk'

##
fitsfile1 = '/dc2/dc2/u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z/calexp/20240805/i/i_sim_1.4/635810/calexp_LSSTCam-imSim_i_i_sim_1_4_635810_R01_S01_u_nsedaghat_Dataset0_1_1-sciCalexps_20220521T042355Z.fits'

butler = Butler('/dc2/dc2/')
dataId = {'instrument': 'LSSTCam-imSim',
          'visit': 635810,
          'detector': 1}

run_collection = butler.registry.queryCollections(f'u/nsedaghat/RegeneratedCalexps_{tag}/*')
if len(run_collection) != 1:
    raise RuntimeError(f'Found {len(run_collection)} collections for {tag}')
run_collection = run_collection[0]

fitsfile2 = butler.getURI('calexp',
                          collections=[run_collection],
                          dataId = dataId)
# convert fitsfile2 to a regular file name
fitsfile2 = str(fitsfile2).split('file:')[1]

print(fitsfile1, fitsfile2)

# Get the images from the calexps
hdu1 = fits.open(fitsfile1)
hdu2 = fits.open(fitsfile2)


im1 = hdu1[1].data
im2 = hdu2[1].data

# Compute the difference
diff = im1 - im2

# Subplot1 : the diff image itself, in zscale
from astropy.visualization import ZScaleInterval
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
zscale = ZScaleInterval()
vmin, vmax = zscale.get_limits(diff)
plt.imshow(diff, vmin=vmin, vmax=vmax, cmap='gray')
plt.colorbar()

plt.suptitle(tag)


# I need to manually display mouse-hovered pixel values,
# due to mal-functioning of the matplotlib's built-in
# cursor display, through an xpra connection.
def on_mouse_move(event):

    if not event.inaxes:
        return

    if event.xdata is None or event.ydata is None:
        return

    # Get the x and y coordinates of the mouse cursor
    x, y = int(event.xdata), int(event.ydata)

    # Check if the cursor is within the bounds of the image
    if 0 <= x < diff.shape[1] and 0 <= y < diff.shape[0]:
        # Get the value of the pixel under the cursor
        value = diff[y, x]

        # Update the figure title to show the pixel value
        plt.xlabel(f'x={x}, y={y}, value={value:g}')
        plt.draw()

fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)


# Show the plot
#plt.savefig(f'compare_calexps_{tag}.png')
plt.show()
