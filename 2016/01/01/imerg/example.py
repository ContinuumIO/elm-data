"""
conda install basemap matplotlib
"""

# This is a sample script that reads and plots the IMERG data.
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import numpy as np
import h5py as h5py

dataset = h5py.File('3B-MO.MS.MRG.3IMERG.20160101-S000000-E235959.01.V03D.HDF5', 'r') # Change this to the proper path

precip = dataset['Grid/precipitation'][:]
precip = np.transpose(precip)

theLats= dataset['Grid/lat'][:]
theLons = dataset['Grid/lon'][:]

# Plot the figure, define the geographic bounds
fig = plt.figure(dpi=300)
latcorners = ([-60,60])
loncorners = ([-180,180])

m = Basemap(projection='cyl',llcrnrlat=latcorners[0],urcrnrlat=latcorners[1],llcrnrlon=loncorners[0],urcrnrlon=loncorners[1])

# Draw coastlines, state and country boundaries, edge of map.
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Draw filled contours.
clevs = np.arange(0,1.26,0.125)
# Define the latitude and longitude data
x, y = np.float32(np.meshgrid(theLons, theLats))

# Mask the values less than 0 because there is no data to plot.
masked_array = np.ma.masked_where(precip < 0,precip)

# Plot every masked value as white
cmap = cm.GMT_drywet
cmap.set_bad('w',1.)

# Plot the data
cs = m.contourf(x,y,precip,clevs,cmap=cmap,latlon=True)
parallels = np.arange(-60.,61,20.)
m.drawparallels(parallels,labels=[True,False,True,False])
meridians = np.arange(-180.,180.,60.)
m.drawmeridians(meridians,labels=[False,False,False,True])

# Set the title and fonts
plt.title('June 2016 Monthly Average Rain Rate')
font = {'weight' : 'bold', 'size' : 6}
plt.rc('font', **font)

# Add colorbar
cbar = m.colorbar(cs,location='right',pad="5%")
cbar.set_label('mm/h')

plt.show()
