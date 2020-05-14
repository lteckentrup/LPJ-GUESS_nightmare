import pandas as pd
import xarray
import os
import datetime
import numpy as np

## Import Data
colnames = ['Lon', 'Lat', 'Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthnames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
              'Oct', 'Nov', 'Dec']

df = pd.read_csv('../global_CRUNCEP_nonoise/mgpp.out', header=0,
                  error_bad_lines=False, names=colnames, delim_whitespace=True)

df_stack = df[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
              'Oct', 'Nov', 'Dec']].stack()

# df_time = pd.date_range('1901-01-01', periods=1380, freq='M')

# Rearrange so all var values are in one column
mgpp = df_stack.to_numpy()
lon = df['Lon'].to_numpy()
lat = df['Lat'].to_numpy()

# time = df_time.to_numpy()
# time = np.arange(1901,2016)
# time = np.repeat(time, repeats = 12)
print(len(np.repeat(lon, repeats = 12)))
print(len(np.arange(0, 81366180)))
# print(len(np.tile(time, 58961)))

# Write into new dataframe
df_sorted = pd.DataFrame()
df_sorted['Lon'] = np.repeat(lon, repeats = 12)
df_sorted['Lat'] = np.repeat(lat, repeats = 12)
# df_sorted['Time'] = np.tile(time, int(len(np.repeat(lon, repeats = 12)/1380)))
# df_sorted['Time'] = np.tile(time, 58961)
df_sorted['Time'] = np.arange(0, 81366180)
df_sorted['mgpp'] = mgpp

print(df_sorted.head)
print(df_sorted.tail)

print(df_sorted.set_index(['Time', 'Lat', 'Lon']))
xr = df_sorted.set_index(['Time', 'Lat', 'Lon']).to_xarray()

# add metadata
xr['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
xr['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}
xr['mgpp'].attrs={'units':'kgC/m2/month', 'long_name':'Monthly GPP'}

# add global attribute metadata
# xr.attrs={'Conventions':'CF-1.6', 'title':'Data', 'summary':'Data generated'}

# save to netCDF
xr.to_netcdf('test.nc', encoding={'Time':{'dtype': 'double'},
                                  'Lat':{'dtype': 'double'}, 
                                  'Lon':{'dtype': 'double'}, 
                                  'mgpp':{'dtype': 'float32'}})
