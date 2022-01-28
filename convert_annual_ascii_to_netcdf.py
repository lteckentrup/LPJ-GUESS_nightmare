import pandas as pd
import xarray as xr
import os
import numpy as np
from datetime import date

date_created = date.today()

def convert_ascii_netcdf(pathway, var, time_res, experiment, setup):

    df = pd.read_csv(pathway+var+'.out',header=0,error_bad_lines=False,
                     delim_whitespace=True)

    years = np.unique(df.Year)
    first_year = str(int(years[0]))
    last_year = str(int(years[-1]))
    print(last_year)
    df2 = df.rename(columns={'Year': 'Time'})
    df2.Time = pd.to_datetime(df2.Time, format = '%Y')

    ds = df2.set_index(['Time', 'Lat', 'Lon']).to_xarray()

    ds.Time.encoding['units'] = 'Seconds since 1901-01-01 00:00:00'
    ds.Time.encoding['long_name'] = 'Time'
    ds.Time.encoding['calendar'] = '365_day'

    # add metadata
    ds['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
    ds['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}

    ## Fill up missing latitudes and longitudes
    dx = ds.Lon - ds.Lon.shift(shifts={'Lon':1})
    dx = dx.min()
    dy = ds.Lat - ds.Lat.shift(shifts={'Lat':1})
    dy = dy.min()

    newlon = np.arange((-180.+dx/2.),180.,dx)
    newlon = xr.DataArray(newlon, dims=("Lon"),coords={"Lon":newlon},
                          attrs=ds.Lon.attrs)

    newlat = np.arange((-90.+dy/2.),90., dy)
    newlat = xr.DataArray(newlat, dims=("Lat"), coords={"Lat":newlat},
                          attrs=ds.Lat.attrs)

    foo = xr.DataArray(np.empty((ds.Time.size, newlat.size, newlon.size)),
                       dims=("Time", "Lat", "Lon"),
                       coords={"Time":ds.Time, "Lat":newlat, "Lon":newlon},
                       name="foo")

    foo[:]=np.NaN
    ds_fill = ds.broadcast_like(foo)

    # add global attributes
    if setup == 'no_dist':
        ds_fill.attrs={'Conventions':'CF-1.6',
                       'Model':'LPJ-GUESS version 4.0.1.',
                       'Set-up': 'Stochastic and fire disturbance not active',
                       'Title':experiment, 'Date_Created':str(date_created)}
    else:
        ds_fill.attrs={'Conventions':'CF-1.6',
                       'Model':'LPJ-GUESS version 4.0.1.',
                       'Set-up': 'Stochastic and fire disturbance active',
                       'Title':experiment, 'Date_Created':str(date_created)}

    fileOUT = pathway+var+'_LPJ-GUESS_'+first_year+'-'+last_year+'.nc'

    dim = ['Time', 'Lat', 'Lon']
    dim_dtype = ['double', 'double', 'double']

    if var in ('aaet', 'agpp', 'anpp', 'clitter', 'cmass', 'cton_leaf', 'dens',
               'fpc', 'height', 'lai', 'nlitter', 'nmass', 'nuptake', 'vmaxnlim'):
        if var == 'aaet':
            unit='mm/year'
        elif var in ('agpp', 'anpp'):
            unit='kgC/m2/year'
        elif var in ('clitter', 'cmass'):
            unit='kgC/m2'
        elif var == 'cton_leaf':
            unit='ckgC/kgN'
        elif var == 'dens':
            unit='indiv/m2'
        elif var in ('fpc', 'lai'):
            unit='m2/m2'
        elif var in ('nlitter', 'nmass'):
            unit='kgN/m2'
        elif var == 'nuptake':
            unit='kgN/m2/year'
        elif var == 'vmaxlim':
             unit='-'
        elif var == 'height':
            unit='m'

        for PFT_short, PFT_long in zip(PFT_shortnames, PFT_longnames):
            ds_fill[PFT_short].attrs={'units':unit,
                                      'long_name':PFT_long}
            dim.append(PFT_short)
            dim_dtype.append('float32')

        if var in ('aaet', 'agpp', 'anpp', 'clitter', 'cmass', 'cton_leaf', 'dens',
                   'fpc', 'lai', 'nlitter', 'nmass', 'nuptake', 'vmaxnlim'):
            ds_fill['Total'].attrs={'units':unit,
                                           'long_name':'Total'}
            dim.append('Total')
            dim_dtype.append('float32')
        else:
            pass

    elif var == 'cflux':
        for cflux_short, cflux_long in zip(cflux_shortnames, cflux_longnames):
            ds_fill[cflux_short].attrs={'units':'kgC/m2/year',
                                        'long_name':cflux_long}

            dim.append(cflux_short)
            dim_dtype.append('float32')

    elif var == 'cpool':
        for cpool_short, cpool_long in zip(cpool_shortnames, cpool_longnames):
            ds_fill[cpool_short].attrs={'units':'kgC/m2',
                                        'long_name':'cpool_long'}

            dim.append(cpool_short)
            dim_dtype.append('float32')

    elif var == 'firert':
        ds_fill['FireRT'].attrs={'units':'yr',
                                 'long_name':'Fire return time'}

        dim.append('FireRT')
        dim_dtype.append('float32')

    elif var == 'doc':
        ds_fill['Total'].attrs={'units':'kgC/m2r',
                                'long_name':'Total dissolved organic carbon'}

        dim.append('Total')
        dim_dtype.append('float32')

    elif var == 'nflux':
        for nflux_short, nflux_long in zip(nflux_shortnames, nflux_longnames):
            ds_fill[nflux_short].attrs={'units':'kgN/ha/year',
                                        'long_name':nflux_long}

            dim.append(nflux_short)
            dim_dtype.append('float32')

    elif var == 'ngases':
        for ngases_short, ngases_long in zip(ngases_shortnames, ngases_longnames):
            ds_fill[ngases_short].attrs={'units':'kgN/ha/year',
                                         'long_name':ngases_long}

            dim.append(ngases_short)
            dim_dtype.append('float32')

    elif var == 'npool':
        for npool_short, npool_long in zip(npool_shortnames, npool_longnames):
            ds_fill[npool_short].attrs={'units':'kgN/m2',
                                        'long_name':npool_long}
            dim.append(npool_short)
            dim_dtype.append('float32')

    elif var == 'nsources':
        for nsources_short, nsources_long in zip(nsources_shortnames,
                                                 nsources_longnames):
            ds_fill[nsources_short].attrs={'units':'gN/ha',
                                           'long_name':nsources_long}

            dim.append(nsources_short)
            dim_dtype.append('float32')

    elif var == 'tot_runoff':
        for tot_runoff_short, tot_runoff_long in zip(tot_runoff_shortnames,
                                                     tot_runoff_longnames):
            ds_fill[tot_runoff_short].attrs={'units':'mm/year',
                                           'long_name':tot_runoff_long}

            dim.append(tot_runoff_short)
            dim_dtype.append('float32')
    else:
        pass

    dtype_fill = ['dtype']*len(dim)
    encoding_dict = {a: {b: c} for a, b, c in zip(dim, dtype_fill, dim_dtype)}

    # save to netCDF
    ds_fill.to_netcdf(fileOUT, encoding=encoding_dict)

### Control CRUNCEP
convert_ascii_netcdf('global_CRUNCEP/', 'agpp', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', '')
convert_ascii_netcdf('global_CRUNCEP/', 'cflux', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', '')
convert_ascii_netcdf('global_CRUNCEP/', 'cpool', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', '')

### Control CRUNCEP without disturbance
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist/', 'agpp', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist/', 'cflux', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist/', 'cpool', 'annual',
                     'LPJ-GUESS output CRUNCEP V7', 'no_dist')

### CP only (anomaly) CRUNCEP without disturbance
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_CP_anomaly/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_CP_anomaly/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_CP_anomaly/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')
