import xarray as xr
import xesmf 

def cmip4lpj(var_cmip,var_lpj,sn_lpj):
    ### insert filename of raw data
    ### Can be single file:
    fname_IN = ''
    ds = xr.open_dataset(fname_IN)

    ### or you can also read in multiple files
    pathwayIN='' ### Insert directory where raw data for GCM are located
    ds = xr.open_mfdataset(pathwayIN+'*nc')
    
    ## Rename variable
    ds = ds.rename({var_cmip:var_lpj})
    ds[var_lpj].attrs['standard_name'] = sn_lpj
    
    ### Only for daily and if you want to harmonise all calendars
    ds = ds.convert_calendar('noleap')

    ### Adjust unit for some variables
    if var_lpj == 'rhum':
        ds[var_lpj] = ds[var_lpj]/100
        ds[var_lpj].attrs['units'] = '1'

    ### Remove bounds (LPJ doesn't need them)
    ds = ds.drop_vars('time_bnds')
    ds = ds.drop_vars('lat_bnds')
    ds = ds.drop_vars('lon_bnds')
    ds = ds.transpose('lat','lon','time')

    ### insert filename of LPJ data
    fname_OUT = ''
    ds.to_netcdf(fname_OUT,
                encoding={'time':{'dtype': 'double'},
                          'lat':{'dtype': 'double'},
                          'lon':{'dtype': 'double'},
                          var_lpj:{'dtype': 'float32'}})

cmip4lpj('tas','temp','air_temperature')
cmip4lpj('pr','prec','precipitation_flux')
cmip4lpj('rsds','insol','surface_downwelling_shortwave_flux')
cmip4lpj('hurs','rhum','relative_humidity')
cmip4lpj('tasmax','tmax','air_temperature')
cmip4lpj('tasmin','tmin','air_temperature')
cmip4lpj('sfcWind','wind','wind_speed')
