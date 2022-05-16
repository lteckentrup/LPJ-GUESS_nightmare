import pandas as pd
import xarray as xr
import os
import numpy as np
from datetime import date
from vars import (
    PFT_shortnames,
    PFT_longnames,
    cflux_shortnames,
    cflux_longnames,
    cpool_shortnames,
    cpool_longnames,
    BA_shortname,
    BA_longname,
    firert_shortnames,
    firert_longnames,
    nflux_shortnames,
    nflux_longnames,
    ngases_shortnames,
    ngases_longnames,
    npool_shortnames,
    npool_longnames,
    nsources_shortnames,
    nsources_longnames,
    simfire_analysis_shortnames,
    simfire_analysis_longnames,
    tot_runoff_shortnames,
    tot_runoff_longnames
    )

date_created = date.today()

def convert_ascii_netcdf_annual(pathway, var):
    ### Pathway to LPJ ASCII
    pathwayIN='/g/data/w97/lt0205/research/lpj_guess_4.1_modify/runs/CRUJRA_GlobFIRM/'

    ### Pathway to directory for LPJ netCDF
    pathwayOUT = 'CRUJRA_GlobFIRM_release/'

    ### Read in ASCII
    df = pd.read_csv(pathwayIN+var+'.out',header=0,on_bad_lines='warn',
                     delim_whitespace=True)

    years = np.unique(df.Year)
    first_year = str(int(years[0]))
    last_year = str(int(years[-1]))

    ### Name LPJ netCDF file
    fileOUT = (pathwayOUT+var+'_LPJ-GUESS_'+first_year+'-'+last_year+'.nc')

    ### Stupid pandas blah
    df2 = df.rename(columns={'Year': 'Time'})
    df2.Time = pd.to_datetime(df2.Time, format = '%Y')
    ds = df2.set_index(['Time', 'Lat', 'Lon']).to_xarray()

    ### Sort time axis
    ds.Time.encoding['units'] = 'Seconds since 1850-01-01 00:00:00'
    ds.Time.encoding['long_name'] = 'Time'
    ds.Time.encoding['calendar'] = '365_day'

    ### Sort latitude and longitude
    ds['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
    ds['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}

    ## Fill up missing latitudes and longitudes
    dx = ds.Lon - ds.Lon.shift(shifts={'Lon':1})
    dy = ds.Lat - ds.Lat.shift(shifts={'Lat':1})
    dx = dx.min()
    dy = dy.min()

    newlon = np.arange((-180.+dx/2.),180.,dx)
    newlon = xr.DataArray(newlon, dims=('Lon'),coords={'Lon':newlon},
                          attrs=ds.Lon.attrs)

    newlat = np.arange((-90.+dy/2.),90., dy)
    newlat = xr.DataArray(newlat, dims=('Lat'), coords={'Lat':newlat},
                          attrs=ds.Lat.attrs)

    foo = xr.DataArray(np.empty((ds.Time.size, newlat.size, newlon.size)),
                       dims=('Time', 'Lat', 'Lon'),
                       coords={'Time':ds.Time, 'Lat':newlat, 'Lon':newlon},
                       name='foo')

    foo[:]=np.NaN
    ds_fill = ds.broadcast_like(foo)

    ### Experiment description for netCDF header
    experiment = 'New release, fire model: BLAZE'

    # add global attributes
    ds_fill.attrs={'Conventions':'CF-1.6',
                   'Model':'LPJ-GUESS version 4.0.1.',
                   'Set-up': 'Stochastic and fire disturbance active',
                   'Title':experiment, 'Date_Created':str(date_created)}

    dim = ['Time', 'Lat', 'Lon']
    dim_dtype = ['double', 'double', 'double']

    ### Add variables to dataset
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
        elif var in ('simfireanalysis', 'vmaxlim'):
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

    elif var == 'annual_burned_area':
        ds_fill[BA_shortname].attrs={'units':'-',
                                     'long_name':BA_longname}

        dim.append(BA_shortname)
        dim_dtype.append('float32')

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
        for firert_short, firert_long in zip(firert_shortnames,firert_longnames):
            ds_fill[firert_short].attrs={'units':'-',
                                         'long_name':firert_long}

            dim.append(firert_short)
            dim_dtype.append('float32')

    elif var == 'doc':
        ds_fill['Total'].attrs={'units':'kgC/m2',
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

    elif var == 'simfireanalysis':
        for simfire_analysis_short, simfire_analysis_long in zip(simfire_analysis_shortnames,
                                                                 simfire_analysis_longnames,):
            ds_fill[simfire_analysis_short].attrs={'units':'-',
                                                   'long_name':simfire_analysis_long}

            dim.append(simfire_analysis_short)
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

def convert_ascii_netcdf_monthly(pathway, var, PFT):
    ### Monthly output can either be total or per PFT
    if PFT == None:
        full_var = var
    else:
        full_var = var+'_'+PFT

    ### Pathway to LPJ ASCII
    pathwayIN='/g/data/w97/lt0205/research/lpj_guess_4.1_modify/runs/CRUJRA_GlobFIRM/'

    ### Pathway to directory for LPJ netCDF
    pathwayOUT = 'CRUJRA_GlobFIRM_release/'

    ### Read in ASCII
    df = pd.read_csv(pathwayIN+var+'.out',header=0,on_bad_lines='warn',
                     delim_whitespace=True)

    years = np.unique(df.Year)

    first_year=str(int(years[0]))
    last_year=str(int(years[-1]))
    nyears = len(years)

    fileOUT = (pathwayOUT+var+'_LPJ-GUESS_'+first_year+'-'+last_year+'.nc')

    months=list(df.columns)
    months=months[3:]

    lons = np.unique(df.Lon)
    lats = np.unique(df.Lat)

    nrows = len(lats)
    ncols = len(lons)
    nmonths = 12

    lons.sort()
    lats.sort()
    years.sort()

    # Create the axes
    time = pd.date_range(start=f'01/{years[0]}',
                         end=f'01/{years[-1]+1}', freq='M')

    # Generic way to create a regular grid from [-180,180] and [-90, 90]
    # when knowing the resolution.

    dx = 0.5
    Lon = xr.DataArray(np.arange(-180.+dx/2., 180., dx),
                       dims=('Lon'),
                       attrs={'long_name':'longitude',
                              'unit':'degrees_east'})
    nlon = Lon.size
    dy = 0.5
    Lat = xr.DataArray(np.arange(-90.+dy/2., 90., dy),
                       dims=('Lat'),
                       attrs={'long_name':'latitude',
                              'unit':'degrees_north;})
    nlat = Lat.size

    out = xr.DataArray(np.zeros((nyears*nmonths,nlat, nlon)),
                       dims=('Time','Lat','Lon'),
                       coords=({'Lat':Lat,
                                'Lon':Lon,
                                'Time':time}))
    out[:] = np.nan

    df_stack = df[months].stack(dropna=False)

    for nr in range(0,len(df.index),nyears):
        rows = df[nr:nr+nyears]
        thislon = rows['Lon'].min()
        thislat = rows['Lat'].min()
        out.loc[dict(
                Lon=thislon,
                Lat=thislat)] = df_stack[nr*nmonths:(nr+nyears)*nmonths]

    out.Time.encoding['units'] = 'Seconds since 1901-01-01 00:00:00'
    out.Time.encoding['long_name'] = 'Time'
    out.Time.encoding['calendar'] = '365_day'

    if PFT==None:
        ds= out.to_dataset(name=var)
    else:
        ds= out.to_dataset(name=var+'_'+PFT)


    experiment = 'New release, fire model: BLAZE'


    ds.attrs={'Conventions':'CF-1.6',
              'Model':'LPJ-GUESS version 4.0.1.',
              'Set-up': 'Stochastic and fire disturbance active',
              'Title':experiment, 'Date_Created':str(date_created)}

    ### Monthly Total
    if var == 'maet':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly actual Evapotranspiration'}
    elif var == 'mevap':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly Evapotranspiration'}
    elif var == 'mgpp':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly GPP'}
    elif var == 'mintercep':
        ds['mintercep'].attrs={'units':'mm/month',
                               'long_name':'Monthly interception Evaporation'}
    elif var == 'miso':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly isopene emissions'}
    elif var == 'mmon':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly monterpene emissions'}
    elif var == 'mnee':
        ds[var].attrs={'units':'kgC/m2/month', 'long_name':'Monthly NEE'}
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

    ### monthly per PFT
    elif var == 'mpaet':
        ds[var+'_'+PFT].attrs={'units':'mm/month',
                               'long_name':'Monthly Actual '
                               'Evapotranspiration '+
                               PFT_longnames[PFT_shortnames.index(PFT)]}
    elif var == 'mpgpp':
        ds[var+'_'+PFT].attrs={'units':'kgC/m2/month',
                               'long_name':'Monthly GPP '+
                               PFT_longnames[PFT_shortnames.index(PFT)]}
    elif var == 'mpnpp':
            ds[var+'_'+PFT].attrs={'units':'kgC/m2/month',
                                         'long_name':'Monthly NPP '+
                                         PFT_longnames[PFT_shortnames.index(PFT)]}
    elif var == 'mpra':
        for PFT_short, PFT_long in zip(PFT_shortnames,PFT_longnames):
            ds[var+'_'+PFT].attrs={'units':'kgC/m2/month',
                                         'long_name':'Monthly Ra '+
                                         PFT_longnames[PFT_shortnames.index(PFT)]}
    elif var == 'mplai':
        for PFT_short, PFT_long in zip(PFT_shortnames,PFT_longnames):
            ds[var+'_'+PFT].attrs={'units':'m2/m2',
                                         'long_name':'Monthly LAI '+
                                         PFT_longnames[PFT_shortnames.index(PFT)]}

    ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                    'Lat':{'dtype': 'double'},
                                    'Lon':{'dtype': 'double'},
                                     full_var:{'dtype': 'float32'}})
