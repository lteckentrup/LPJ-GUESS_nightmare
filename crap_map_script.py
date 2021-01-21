from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as open_ncfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

#-- call  function and plot figure
fig, ax = plt.subplots(figsize=(7.5,6.5))

file = open_ncfile('rx1day_ANN_CCCMA3.1_R1_d01_1990-2009.nc')

### read in coordinates
lat = file.variables['y'][:]*(-1) ### invert latitude (not sure whether that's necessary?)
lon = file.variables['x'][:]

### read in variable and choose the 11th timestep
data = file.variables['rx1day'][10,:,:]

#-- create map, you can change the region by defining the upper and lower lat and lon
map = Basemap(projection='cyl',llcrnrlat= -44.75,urcrnrlat=-10.25,\
              resolution='c',  llcrnrlon=110.,urcrnrlon=160.)

#-- draw coastlines and edge of map
map.drawcoastlines()
x, y = map(*np.meshgrid(lon, lat))

cut_data = data[:-1, :-1]
cmap = plt.cm.viridis_r

### Reduce white areas
plt.subplots_adjust(top=0.95, left=0.02, right=0.98, bottom=0.10,
                    wspace=0.03, hspace=0.15)

plt.title('Rx1day Australia')

levels = np.arange(0,110,10)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
cnplot = map.pcolormesh(x, y, cut_data, cmap=cmap, norm=norm)

### Move colorbar horizontal or vertical direction, make it wider or change height
cax = plt.axes([0.2, 0.1, 0.6, 0.02])

### Decide whether horizonal or vertical orientation
cbar=fig.colorbar(cnplot, orientation='horizontal', cax=cax)
cbar.ax.tick_params(labelsize=10)
plt.colorbar(ticks = levels, cax=cax, orientation='horizontal')
cbar.set_label('Random PPT stat',fontsize=10)

### Helps you manage white space

plt.subplot_tool()
plt.show()
# plt.savefig('crap.png', dpi = 500)
