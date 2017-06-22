"""
==============================
Edge Enhancing Filtering a Map
==============================

This example shows how to edge enhance a coronal loops in an SDO/AIA image.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

import astropy.units as u
from astropy.coordinates import SkyCoord

from sunpy.map import Map
from sunpy.data.sample import AIA_171_IMAGE

###############################################################################
# We first create the Map using the sample data and make a submap of a region
# with some interesting loop features.
aia = Map(AIA_171_IMAGE)
bl = SkyCoord(750*u.arcsec, -200*u.arcsec, frame=aia.coordinate_frame)
tr = SkyCoord(1500*u.arcsec, 550*u.arcsec, frame=aia.coordinate_frame)
aia_smap = aia.submap(bl, tr)
###############################################################################
# Next we apply an edge enhance filter to the data in both x and y directions
# and combine the two images together.
sx = ndimage.sobel(aia_smap.data, axis=0, mode='constant')
sy = ndimage.sobel(aia_smap.data, axis=1, mode='constant')
edge_enhanced_im = np.hypot(sx, sy)

###############################################################################
# Finally we create a new map with the edge enhanced data and plot the result.
edge_map = Map(edge_enhanced_im, aia_smap.meta)

plt.figure(figsize=(12, 4))
plt.subplot(121)
aia_smap.plot()
plt.subplot(122)
edge_map.plot()
#plt.savefig("gallery_sharp.png")
plt.show()
