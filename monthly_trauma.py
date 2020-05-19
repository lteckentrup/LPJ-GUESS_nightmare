import pandas as pd
import numpy as np
import xarray as xr

fname = "global_CRUNCEP/mgpp.out"
df = pd.read_csv(fname, header=0, delim_whitespace=True)

months=list(df.columns)
months=months[3:]

lons = np.unique(df.Lon)
lats = np.unique(df.Lat)
years = np.unique(df.Year)
nyears = len(years)
nrows = len(lats)
ncols = len(lons)
nmonths = 12
lons.sort()
lats.sort()
years.sort()

# Create the axes
time = pd.date_range(start=f'01/{years[0]}',
                     end=f'01/{years[-1]+1}', freq='M')
# We'll use a generic way to create a regular grid from [-180,180] and
# [-90, 90] when knowing the resolution. Feel free to reuse as needed.
dx = 0.5
Lon = xr.DataArray(np.arange(-180.+dx/2., 180., dx), dims=("Lon"),
                   attrs={"long_name":"longitude", "unit":"degrees_east"})
nlon = Lon.size
dy = 0.5
Lat = xr.DataArray(np.arange(-90.+dy/2., 90., dy), dims=("Lat"),
                   attrs={"long_name":"latitude", "unit":"degrees_north"})
nlat = Lat.size

out = xr.DataArray(np.zeros((nyears*nmonths, nlat, nlon)),
                   dims=("Time","Lat","Lon"),
                   coords=({"Time":time, "Lat":Lat, "Lon":Lon}))
out[:] = np.nan
row = next(df.iterrows())[1]
print(row)
print(row[3:])

out.loc[dict(
        Time=out.Time[(out.Time.dt.year==row["Year"])],
        Lat=out.Lat[(out.Lat==row["Lat"])],
        Lon=out.Lon[(out.Lon==row["Lon"])])] = row[3:].to_numpy().reshape(12,1,1)

df_stack = df[months].stack()

rows = df[0:nyears]
# If we had missing years, we could add the missing years rows and then
# stack only the rows for the point here.
#rows_stack = rows[months].stack()
out.loc[dict(
        Lat=out.Lat[(out.Lat==rows["Lat"].min())],
        Lon=out.Lon[(out.Lon==rows["Lon"].min())])] = df_stack[0:nyears*nmonths].to_numpy().reshape(1380,1,1)
out.sel(Lat=rows["Lat"].min(),Lon=rows["Lon"].min())

for nr in range(0,len(df.index),nyears):
    print(nr)
    rows = df[nr:nr+nyears]
    thislat = rows["Lat"].min()
    thislon = rows["Lon"].min()
    out.loc[dict(
            Lat=out.Lat[(out.Lat==thislat)],
            Lon=out.Lon[(out.Lon==thislon)])] = df_stack[nr*nmonths:(nr+nyears)*nmonths]

out.Time.encoding['units'] = 'Seconds since 1901-01-01 00:00:00'
out.Time.encoding['long_name'] = 'Time'
out.Time.encoding['calendar'] = '365_day'

ds = out.to_dataset(name='mgpp')

ds.to_netcdf('out.nc', encoding={'Time':{'dtype': 'double'},
                                 'Lat':{'dtype': 'double'},
                                 'Lon':{'dtype': 'double'},
                                 'mgpp':{'dtype': 'float32'}})
