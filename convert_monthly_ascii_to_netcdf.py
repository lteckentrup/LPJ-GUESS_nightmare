import pandas as pd
import numpy as np
import xarray as xr
from datetime import date

pathway= 'global_CRUNCEP/'
# pathway= 'global_CRUNCEP_only_CP_anomaly_npatch_100/'
# pathway= 'global_CRUNCEP_only_EP_anomaly_npatch_100/'
# pathway= 'global_CRUNCEP_only_CP_nearest_year_npatch_100/'
# pathway= 'global_CRUNCEP_only_EP_nearest_year_npatch_100/'
# pathway='global_CRUNCEP_no_fire_no_dist_npatch_100/'
# pathway='global_CRUNCEP_no_fire_no_dist_only_EP_anomaly_npatch_100/'
# pathway='global_CRUNCEP_no_fire_no_dist_only_CP_anomaly_npatch_100/'
# pathway='binary/'

date_created = date.today()
def convert_ascii_netcdf_monthly(var, time_res, experiment, setup):
    fname = pathway+var+'.out'
    df = pd.read_csv(fname, header=0, delim_whitespace=True)

    months=list(df.columns)
    months=months[3:]

    lons = np.unique(df.Lon)
    lats = np.unique(df.Lat)
    years = np.unique(df.Year)
    first_year=str(int(years[0]))
    last_year=str(int(years[-1]))
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

    out = xr.DataArray(np.zeros((nyears*nmonths,nlat, nlon)),
                       dims=("Time","Lat","Lon"),
                       coords=({"Lat":Lat, "Lon":Lon, "Time":time}))
    out[:] = np.nan
    df_stack = df[months].stack()

    for nr in range(0,len(df.index),nyears):
        print(nr)
        rows = df[nr:nr+nyears]
        thislon = rows["Lon"].min()
        thislat = rows["Lat"].min()
        out.loc[dict(
                Lon=thislon,
                Lat=thislat)] = df_stack[nr*nmonths:(nr+nyears)*nmonths]

    out.Time.encoding['units'] = 'Seconds since 1901-01-01 00:00:00'
    out.Time.encoding['long_name'] = 'Time'
    out.Time.encoding['calendar'] = '365_day'

    ds = out.to_dataset(name='mgpp')

    if setup == 'no_dist':
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance not active',
                  'Title':experiment, 'Date_Created':str(date_created)}
    else:
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance active',
                  'Title':experiment, 'Date_Created':str(date_created)}

    fileOUT = pathway+var+'_LPJ-GUESS_'+first_year+'-'+last_year+'.nc'

    if var == 'maet':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly actual Evapotranspiration'}
    elif var == 'mevap':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly Evapotranspiration'}
    elif var == 'mgpp':
        ds[var].attrs={'units':'kgC/m2/month', 'long_name':'Monthly GPP'}
    elif var == 'mintercep':
        ds['mintercep'].attrs={'units':'mm/month',
                               'long_name':'Monthly interception Evaporation'}
    elif var == 'miso':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly isopene emissions'}
    elif var == 'miso':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly monterpene emissions'}
    elif var == 'mmon':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly isoprene emissions'}
    elif var == 'mnee':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly NEE'}
    elif var == 'mnpp':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly NPP'}
    elif var == 'mpet':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly potential evapotranspiration'}
    elif var == 'mra':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly autotrophic respiration'}
    elif var == 'mrh':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly heterotrophic respiration'}
    elif var == 'mlai':
        ds[var].attrs={'units':'m2/m2',
                       'long_name':'Monthly LAI'}
    elif var == 'mrunoff':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly runoff'}
    elif var == 'mwcont_lower':
        ds[var].attrs={'units':'fraction of available water-holding capacity',
                       'long_name':'Monthly water in content in lower soil layer'
                       '(50 - 150 cm)'}
    elif var == 'mwcont_upper':
        ds[var].attrs={'units':'fraction of available water-holding capacity',
                       'long_name':'Monthly water in content in upper soil layer'
                       '(0 - 50 cm)'}
    ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                    'Lat':{'dtype': 'double'},
                                    'Lon':{'dtype': 'double'},
                                     var:{'dtype': 'float32'}})
convert_ascii_netcdf_monthly('mgpp', 'monthly', 'LPJ-GUESS output CRUNCEP V7', '')
