import pandas as pd
import xarray as xr
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

df_time = pd.date_range('1901-01-01', periods=1380, freq='M')

time = df_time.to_numpy()
mgpp = df_stack.to_numpy()
lon = df['Lon'].to_numpy()
lat = df['Lat'].to_numpy()

data_set=xr.Dataset(coords={'lon': (['x', 'y'], lon),
                            'lat': (['x', 'y'], lat),
                            'time': time})
# temp=np.array([[25, 24, 20, -12],[23, 21, 22, -11]])
data_set["Temperature"]=(['x', 'y', 'time'],  mgpp)
