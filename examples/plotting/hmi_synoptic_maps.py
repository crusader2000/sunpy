# coding: utf-8
"""
==============================================
Loading an HMI daily synoptic image into a Map
==============================================

In this example we load the Daily Synoptic Maps produced by the HMI team. This
data is an interesting demonstration of SunPy's Map class as it is not in the
more common Helioprojective coordinate system, it is in Heliographic Carrington
coordinates and in a non-trivial Cylindrical Equal Area projection.
"""
import numpy as np
import matplotlib.pyplot as plt

from astropy.utils.data import download_file

import sunpy.map

###############################################################################
# Let's download the file and read it into a Map
filename = download_file(
    'http://jsoc.stanford.edu/data/hmi/synoptic/hmi.Synoptic_Mr.2191.fits', cache=True)
syn_map = sunpy.map.Map(filename)

###############################################################################
# There are a couple of oddities with this file, firstly the value of 'CUNIT2':
print(syn_map.meta['CUNIT2'])

###############################################################################
# That is not a unit! What this is telling us is that the latitude coordinate
# is actually the sine of latitude. This is a cyclindrical equal area (CEA)
# projection, which can be checed by looking at the CTYPE keywords.
print(syn_map.meta['CTYPE1'])
print(syn_map.meta['CTYPE2'])

###############################################################################
# With reference to the Thompson (2006) paper
# section 5.5 (https://doi.org/10.1051/0004-6361:20054262),
# CUNIT2 should be in degrees and CDELT2 should be 180/pi times the spacing in
# sin(latitude).
#
# In addition the value of CDELT1 has the wrong sign so let's also fix this.
syn_map.meta['CUNIT2'] = 'degree'
syn_map.meta['CDELT2'] = 180 / np.pi * syn_map.meta['CDELT2']

syn_map.meta['CDELT1'] *= -1

###############################################################################
# Let's also fix the plot settings
syn_map.plot_settings['cmap'] = 'hmimag'
syn_map.plot_settings['norm'] = plt.Normalize(-1500, 1500)

###############################################################################
# Let's plot the results
fig = plt.figure(figsize=(12, 5))
axes = plt.subplot(projection=syn_map)
im = syn_map.plot()

# Set up the Sine Latitude Grid
x = axes.coords[0]
y = axes.coords[1]

x.set_coord_type('longitude', coord_wrap=360.)
y.set_coord_type('latitude')

x.set_major_formatter('dd')
y.set_major_formatter('dd')

x.set_axislabel("Carrington Longitude [deg]")
y.set_axislabel("Latitude [deg]")

x.set_ticks(color='black', exclude_overlapping=True)
y.set_ticks(color='black', exclude_overlapping=True)

axes.coords.grid(color='black', alpha=0.6, linestyle='dotted', linewidth=0.5)

cb = plt.colorbar(im, fraction=0.019, pad=0.1)
cb.set_label("LOS Magnetic Field [Gauss]")

# Another horrible hack to make the ticks draw on the RHS
axes.set_ylim((1, syn_map.data.shape[0] - 1))
plt.title("{} {}-{}".format(syn_map.meta['content'], syn_map.meta['CAR_ROT'],
                            syn_map.meta['CAR_ROT'] + 1))
plt.show()
