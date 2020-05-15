import pandas as pd
import numpy as np
import xarray as xr

fname = "../global_CRUNCEP_nonoise/mgpp.out"
df = pd.read_csv(fname, header=0, delim_whitespace=True)
lons = np.unique(df.Lon)
lats = np.unique(df.Lat)
years = np.unique(df.Year)
nyears = len(years)
nrows = len(lats)
ncols = len(lons)
nmonths = 12
out = np.zeros((nrows, ncols, nyears*nmonths))

df = df.sort_values(['Lat', 'Lon', 'Year'],
                    ascending=[False, False, True]).reset_index(drop=True)

out = np.zeros((nrows, ncols, nyears*nmonths))
for i,lat in enumerate(lats):
    print(i, nrows)
    for j,lon in enumerate(lons):
        vals = df[(df.Lat == lat) & (df.Lon == lon)].values[:,3:]
        if len(vals)> 0:
            vals = vals.reshape(nyears*nmonths)
            out[i,j,:] = vals

t1 = pd.to_datetime('1/1/1901')
time = t1 + pd.to_timedelta(np.arange(nmonths*nyears), 'M')

ds = xr.Dataset(data_vars={"mgpp":(["y", "x", "time"],out)},
                coords={"lat": (["y"], lats),
                        "lon": (["x"], lons),
                        "time": time})
ds.to_netcdf('lina_crap.nc')
