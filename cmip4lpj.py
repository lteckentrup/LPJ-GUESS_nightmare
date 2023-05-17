import xarray as xr
import xesmf 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--var_cmip', type=str, required=True)
parser.add_argument('--var_lpj', type=str, required=True)
parser.add_argument('--sn_lpj', type=str, required=True)
args = parser.parse_args()

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
    
    ### Drop height variable in tas, tasmax, tasmin
    if var_lpj in ('tas','tasmax','tasmin'):
        ds = ds.drop_vars('height')

    ds = ds.transpose('lat','lon','time')

    ### insert filename of LPJ data
    fname_OUT = ''
    ds.to_netcdf(fname_OUT,
                encoding={'time':{'dtype': 'double'},
                          'lat':{'dtype': 'double'},
                          'lon':{'dtype': 'double'},
                          var_lpj:{'dtype': 'float32'}})

cmip4lpj(args.var_cmip,args.var_lpj,args.sn_lpj)

'''
From command line you can then run
python cmip4lpj.py --var_cmip 'tas' --var_lpj 'temp' --sn_lpj 'air_temperature'
python cmip4lpj.py --var_cmip 'pr' --var_lpj 'prec' --sn_lpj 'precipitation_flux'
python cmip4lpj.py --var_cmip 'rsds','insol' --sn_lpj 'surface_downwelling_shortwave_flux'
python cmip4lpj.py --var_cmip 'hurs' --var_lpj 'rhum' --sn_lpj 'relative_humidity'
python cmip4lpj.py --var_cmip 'tasmax' --var_lpj 'tmax' --sn_lpj 'air_temperature'
python cmip4lpj.py --var_cmip 'tasmin' --var_lpj 'tmin' --sn_lpj 'air_temperature'
python cmip4lpj.py --var_cmip 'sfcWind' --var_lpj 'wind' --sn_lpj 'wind_speed'
'''
