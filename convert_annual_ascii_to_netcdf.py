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

    if var in ('aaet', 'agpp', 'clitter', 'cmass', 'cton_leaf', 'dens', 'npp',
               'fpc', 'lai', 'nlitter', 'nmass', 'nuptake', 'vmaxnlim'):

        ds_fill['BNE'].attrs={'units':'kgC/m2/year',
                              'long_name':'Boreal Needleleaved Evergreen tree'}
        ds_fill['BINE'].attrs={'units':'kgC/m2/year',
                               'long_name':'Boreal Needleleaved Evergreen '
                               'shade-Intolerant tree'}
        ds_fill['BNS'].attrs={'units':'kgC/m2/year',
                              'long_name':'Boreal Needleleaved '
                              'Summergreen tree'}
        ds_fill['TeNE'].attrs={'units':'kgC/m2/year',
                               'long_name':'Temperate Needleleaved '
                               'Evergreen tree'}
        ds_fill['TeBS'].attrs={'units':'kgC/m2/year',
                               'long_name':'Temperate (shade-tolerant) '
                               'Broadleaved Summergreen tree'}
        ds_fill['IBS'].attrs={'units':'kgC/m2/year',
                              'long_name':'boreal/ temperate shade-Intolerant '
                              'Broadleaved Summergreen tree'}
        ds_fill['TeBE'].attrs={'units':'kgC/m2/year',
                               'long_name':'Temperate Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrBE'].attrs={'units':'kgC/m2/year',
                               'long_name':'Tropical Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrIBE'].attrs={'units':'kgC/m2/year',
                                'long_name':'Tropical Broadleaved Evergreen '
                                'shade-Intolerant tree'}
        ds_fill['TrBR'].attrs={'units':'kgC/m2/year',
                               'long_name':'Tropical Broadleaved Raingreen '
                               'tree'}
        ds_fill['C3G'].attrs={'units':'kgC/m2/year',
                              'long_name':'(cool) C3 Grass'}
        ds_fill['C4G'].attrs={'units':'kgC/m2/year',
                              'long_name':'(warm) C4 Grass'}
        ds_fill['Total'].attrs={'units':'kgC/m2/year', 'long_name':'Total'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Total':{'dtype': 'float32'},
                                             'BNE':{'dtype': 'float32'},
                                             'BINE':{'dtype': 'float32'},
                                             'BNS':{'dtype': 'float32'},
                                             'TeNE':{'dtype': 'float32'},
                                             'TeBS':{'dtype': 'float32'},
                                             'IBS':{'dtype': 'float32'},
                                             'TeBE':{'dtype': 'float32'},
                                             'TrBE':{'dtype': 'float32'},
                                             'TrIBE':{'dtype': 'float32'},
                                             'TrBR':{'dtype': 'float32'},
                                             'C3G':{'dtype': 'float32'},
                                             'C4G':{'dtype': 'float32'}})

    elif var == 'cflux':
        ds_fill['Veg'].attrs={'units':'kgC/m2/year',
                              'long_name':'Vegetation NPP'}
        ds_fill['Repr'].attrs={'units':'kgC/m2/year',
                               'long_name':'Respired litter derived from '
                               'plant allocation to reproduction'}
        ds_fill['Soil'].attrs={'units':'kgC/m2/year',
                               'long_name':'Soil heterotrophic respiration'}
        ds_fill['Fire'].attrs={'units':'kgC/m2/year',
                               'long_name':'Wildfire emissions'}
        ds_fill['Est'].attrs={'units':'kgC/m2/year',
                              'long_name':'Biomass of plants establishing in '
                              'the current year'}
        ds_fill['NEE'].attrs={'units':'kgC/m2/year', 'long_name':'Net C flux '
                              '(sum of other fluxes'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Veg':{'dtype': 'float32'},
                                             'Repr':{'dtype': 'float32'},
                                             'Soil':{'dtype': 'float32'},
                                             'Fire':{'dtype': 'float32'},
                                             'Est':{'dtype': 'float32'},
                                             'NEE':{'dtype': 'float32'}})

    elif var == 'cpool':
        ds_fill['VegC'].attrs={'units':'kgC/m2',
                               'long_name':'Vegetation carbon pool'}
        ds_fill['LitterC'].attrs={'units':'kgC/m2',
                                  'long_name':'Litter carbon pool'}
        ds_fill['SoilC'].attrs={'units':'kgC/m2',
                                'long_name':'Soil carbon pool'}
        ds_fill['Total'].attrs={'units':'kgC/m2',
                                'long_name':'Total carbon pool'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'VegC':{'dtype': 'float32'},
                                             'LitterC':{'dtype': 'float32'},
                                             'SoilC':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'doc':
        ds_fill['Total'].attrs={'units':'kgC/m2r',
                                'long_name':'Total dissolved organic carbon'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'nflux':
        ds_fill['dep'].attrs={'units':'kgN/ha',
                              'long_name':'Deposition'}
        ds_fill['fix'].attrs={'units':'kgN/ha',
                              'long_name':'Fixation'}
        ds_fill['fert'].attrs={'units':'kgN/ha',
                               'long_name':'fertilization'}
        ds_fill['flux'].attrs={'units':'kgN/ha',
                               'long_name':'Soil emission'}
        ds_fill['leach'].attrs={'units':'kgN/ha',
                                'long_name':'leaching'}
        ds_fill['NEE'].attrs={'units':'kgN/ha',
                              'long_name':'Net N flux (sum of other fluxes)'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'dep':{'dtype': 'float32'},
                                             'fix':{'dtype': 'float32'},
                                             'fert':{'dtype': 'float32'},
                                             'flux':{'dtype': 'float32'},
                                             'leach':{'dtype': 'float32'},
                                             'NEE':{'dtype': 'float32'}})


    elif var == 'ngases':
        ds_fill['NH3'].attrs={'units':'kgN/ha/year',
                              'long_name':'NH3 flux to atmosphere from fire'}
        ds_fill['NOx'].attrs={'units':'kgN/ha/year',
                              'long_name':'NOx flux to atmosphere from fire'}
        ds_fill['N2O'].attrs={'units':'kgN/ha/year',
                              'long_name':'N2O flux to atmosphere from fire'}
        ds_fill['N2'].attrs={'units':'kgN/ha',
                             'long_name':'N2O flux to atmosphere from fire'}
        ds_fill['NSoil'].attrs={'units':'kgN/ha', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'kgN/ha', 'long_name':'Total'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'NH3':{'dtype': 'float32'},
                                             'NOx':{'dtype': 'float32'},
                                             'N2O':{'dtype': 'float32'},
                                             'N2':{'dtype': 'float32'},
                                             'NSoil':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'npool':
        ds_fill['VegN'].attrs={'units':'kgN/m2',
                               'long_name':'Vegetation nitrogen pool'}
        ds_fill['LitterN'].attrs={'units':'kgN/m2',
                                  'long_name':'Litter nitrogen pool'}
        ds_fill['SoilN'].attrs={'units':'kgN/m2',
                                'long_name':'Soil nitrogen pool'}
        ds_fill['Total'].attrs={'units':'kgN/m2',
                                'long_name':'Total nitrogen pool'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'VegN':{'dtype': 'float32'},
                                             'LitterN':{'dtype': 'float32'},
                                             'SoilN':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'nsources':
        ds_fill['dep'].attrs={'units':'gN/ha', 'long_name':'Deposition'}
        ds_fill['fix'].attrs={'units':'gN/ha', 'long_name':'Fixation'}
        ds_fill['fert'].attrs={'units':'gN/ha', 'long_name':'fertilization'}
        ds_fill['input'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['min'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['imm'].attrs={'units':'gN/ha',
                              'long_name':'Nitrogen immobilisation'}
        ds_fill['netmin'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'gN/ha', 'long_name':'Total'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'dep':{'dtype': 'float32'},
                                             'fix':{'dtype': 'float32'},
                                             'fert':{'dtype': 'float32'},
                                             'input':{'dtype': 'float32'},
                                             'min':{'dtype': 'float32'},
                                             'imm':{'dtype': 'float32'},
                                             'netmin':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'tot_runoff':
        ds_fill['Surf'].attrs={'units':'mm/year',  'long_name':'Surface runoff'}
        ds_fill['Drain'].attrs={'units':'mm/year', 'long_name':'??'}
        ds_fill['Base'].attrs={'units':'mm/year', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'mm/year', 'long_name':'??'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Surf':{'dtype': 'float32'},
                                             'Drain':{'dtype': 'float32'},
                                             'Base':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})
    else:
        pass

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

### EP only (anomaly) CRUNCEP without disturbance
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_EP_anomaly/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_EP_anomaly/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_no_fire_no_dist_only_EP_anomaly/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')

### CP only (anomaly) CRUNCEP
convert_ascii_netcdf('global_CRUNCEP_only_CP_anomaly/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_CP_anomaly/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_CP_anomaly/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(anomaly replacement)', 'no_dist')

### CP only (nearest year) CRUNCEP
convert_ascii_netcdf('global_CRUNCEP_only_CP_nearest_year/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(nearest year replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_CP_nearest_year/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(nearest year replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_CP_nearest_year/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only CP El Nino events '
                     '(nearest year replacement)', 'no_dist')

### EP only (anomaly) CRUNCEP
convert_ascii_netcdf('global_CRUNCEP_only_EP_anomaly/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_EP_anomaly/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_EP_anomaly/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(anomaly replacement)', 'no_dist')

### EP only (nearest year) CRUNCEP
convert_ascii_netcdf('global_CRUNCEP_only_EP_nearest_year/', 'agpp',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(nearest year replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_EP_nearest_year/', 'cflux',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(nearest year replacement)', 'no_dist')
convert_ascii_netcdf('global_CRUNCEP_only_EP_nearest_year/', 'cpool',
                     'annual',
                     'LPJ-GUESS output CRUNCEP V7, only EP El Nino events '
                     '(nearest year replacement)', 'no_dist')

### Control GSWP3
convert_ascii_netcdf('global_GSWP3_noleap/', 'agpp', 'annual',
                     'LPJ-GUESS output GSWP3 V2017', '')
convert_ascii_netcdf('global_GSWP3_noleap/', 'cflux', 'annual',
                     'LPJ-GUESS output GSWP3 V2017', '')
convert_ascii_netcdf('global_GSWP3_noleap/', 'cpool', 'annual',
                     'LPJ-GUESS output GSWP3 V2017', '')

### CP only (anomaly) GSWP3
convert_ascii_netcdf('global_GSWP3_noleap_only_CP_anomaly/', 'agpp', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only CP El Nino events '
                     '(anomaly replacement)', '')
convert_ascii_netcdf('global_GSWP3_noleap_only_CP_anomaly/', 'cflux', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only CP El Nino events '
                     '(anomaly replacement)', '')
convert_ascii_netcdf('global_GSWP3_noleap_only_CP_anomaly/', 'cpool', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only CP El Nino events '
                     '(anomaly replacement)', '')

### EP only (anomaly) GSWP3
convert_ascii_netcdf('global_GSWP3_noleap_only_EP_anomaly/', 'agpp', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only EP El Nino events '
                     '(anomaly replacement)', '')
convert_ascii_netcdf('global_GSWP3_noleap_only_EP_anomaly/', 'cflux', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only EP El Nino events '
                     '(anomaly replacement)', '')
convert_ascii_netcdf('global_GSWP3_noleap_only_EP_anomaly/', 'cpool', 'annual',
                     'LPJ-GUESS output GSWP3 V2017, only EP El Nino events '
                     '(anomaly replacement)', '')
