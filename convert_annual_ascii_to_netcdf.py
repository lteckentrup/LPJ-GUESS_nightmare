import pandas as pd
import xarray as xr
import os
import numpy as np
from datetime import date

## Define pathway
pathway=''

date_created = date.today()

def convert_ascii_netcdf(var, time_res, experiment, setup):
    
    df = pd.read_csv(pathway+var+'.out',header=0,error_bad_lines=False, 
                     delim_whitespace=True)
    
    years = np.unique(df.Year)
    nyears = len(years)
    first_year = '1901'
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

    # add global attributes    
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
    
    if var in ('aaet', 'agpp', 'clitter', 'cmass', 'cton_leaf', 'dens', 'npp', 
               'fpc', 'lai', 'nlitter', 'nmass', 'nuptake', 'vmaxnlim'):

        ds['BNE'].attrs={'units':'kgC/m2/year',
                         'long_name':'Boreal Needleleaved Evergreen tree'}
        ds['BINE'].attrs={'units':'kgC/m2/year',
                          'long_name':'Boreal Needleleaved Evergreen '
                          'shade-Intolerant tree'}
        ds['BNS'].attrs={'units':'kgC/m2/year', 
                         'long_name':'Boreal Needleleaved Summergreen tree'}
        ds['TeNE'].attrs={'units':'kgC/m2/year',
                          'long_name':'Temperate Needleleaved Evergreen tree'}
        ds['TeBS'].attrs={'units':'kgC/m2/year',
                          'long_name':'Temperate (shade-tolerant) Broadleaved '
                          'Summergreen tree'}
        ds['IBS'].attrs={'units':'kgC/m2/year',
                         'long_name':'boreal/ temperate shade-Intolerant '
                         'Broadleaved Summergreen tree'}
        ds['TeBE'].attrs={'units':'kgC/m2/year',
                          'long_name':'Temperate Broadleaved Evergreen tree'}
        ds['TrBE'].attrs={'units':'kgC/m2/year',
                          'long_name':'Tropical Broadleaved Evergreen tree'}
        ds['TrIBE'].attrs={'units':'kgC/m2/year',
                           'long_name':'Tropical Broadleaved Evergreen '
                           'shade-Intolerant tree'}
        ds['TrBR'].attrs={'units':'kgC/m2/year',
                          'long_name':'Tropical Broadleaved Raingreen tree'}
        ds['C3G'].attrs={'units':'kgC/m2/year', 'long_name':'(cool) C3 Grass'}
        ds['C4G'].attrs={'units':'kgC/m2/year', 'long_name':'(warm) C4 Grass'}
        ds['Total'].attrs={'units':'kgC/m2/year', 'long_name':'Total'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
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
        ds['Veg'].attrs={'units':'kgC/m2/year',
                         'long_name':'Vegetation NPP'}
        ds['Repr'].attrs={'units':'kgC/m2/year',
                          'long_name':'Respired litter derived from plant '
                          'allocation to reproduction'}
        ds['Soil'].attrs={'units':'kgC/m2/year',
                          'long_name':'Soil heterotrophic respiration'}
        ds['Fire'].attrs={'units':'kgC/m2/year',
                          'long_name':'Wildfire emissions'}
        ds['Est'].attrs={'units':'kgC/m2/year',
                         'long_name':'Biomass of plants establishing in the '
                         'current year'}
        ds['NEE'].attrs={'units':'kgC/m2/year', 'long_name':'Net C flux '
                         '(sum of other fluxes'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'Veg':{'dtype': 'float32'},
                                        'Repr':{'dtype': 'float32'},
                                        'Soil':{'dtype': 'float32'},
                                        'Fire':{'dtype': 'float32'},
                                        'Est':{'dtype': 'float32'},
                                        'NEE':{'dtype': 'float32'}})
            
    elif var == 'cpool':
        ds['VegC'].attrs={'units':'kgC/m2',
                          'long_name':'Vegetation carbon pool'}
        ds['LitterC'].attrs={'units':'kgC/m2',
                             'long_name':'Litter carbon pool'}
        ds['SoilC'].attrs={'units':'kgC/m2',
                           'long_name':'Soil carbon pool'}
        ds['Total'].attrs={'units':'kgC/m2',
                           'long_name':'Total carbon pool'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'VegC':{'dtype': 'float32'},
                                        'LitterC':{'dtype': 'float32'},
                                        'SoilC':{'dtype': 'float32'},
                                        'Total':{'dtype': 'float32'}})
        
    elif var == 'doc':
        ds['Total'].attrs={'units':'kgC/m2r',
                           'long_name':'Total dissolved organic carbon'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'Total':{'dtype': 'float32'}})

    elif var == 'nflux':
        ds['dep'].attrs={'units':'kgN/ha',
                         'long_name':'Deposition'}
        ds['fix'].attrs={'units':'kgN/ha',
                         'long_name':'Fixation'}
        ds['fert'].attrs={'units':'kgN/ha',
                          'long_name':'fertilization'}
        ds['flux'].attrs={'units':'kgN/ha',
                          'long_name':'Soil emission'}
        ds['leach'].attrs={'units':'kgN/ha',
                           'long_name':'leaching'}
        ds['NEE'].attrs={'units':'kgN/ha',
                         'long_name':'Net N flux (sum of other fluxes)'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'dep':{'dtype': 'float32'},
                                        'fix':{'dtype': 'float32'},
                                        'fert':{'dtype': 'float32'},
                                        'flux':{'dtype': 'float32'},
                                        'leach':{'dtype': 'float32'},
                                        'NEE':{'dtype': 'float32'}})
                
                
    elif var == 'ngases':
        ds['NH3'].attrs={'units':'kgN/ha/year',
                         'long_name':'NH3 flux to atmosphere from fire'}
        ds['NOx'].attrs={'units':'kgN/ha/year',
                         'long_name':'NOx flux to atmosphere from fire'}
        ds['N2O'].attrs={'units':'kgN/ha/year',
                         'long_name':'N2O flux to atmosphere from fire'}
        ds['N2'].attrs={'units':'kgN/ha',
                        'long_name':'N2O flux to atmosphere from fire'}
        ds['NSoil'].attrs={'units':'kgN/ha', 'long_name':'??'}
        ds['Total'].attrs={'units':'kgN/ha', 'long_name':'Total'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'NH3':{'dtype': 'float32'},
                                        'NOx':{'dtype': 'float32'},
                                        'N2O':{'dtype': 'float32'},
                                        'N2':{'dtype': 'float32'},
                                        'NSoil':{'dtype': 'float32'},
                                        'Total':{'dtype': 'float32'}})            
                
    elif var == 'npool':
        ds['VegN'].attrs={'units':'kgN/m2', 
                          'long_name':'Vegetation nitrogen pool'}
        ds['LitterN'].attrs={'units':'kgN/m2',
                             'long_name':'Litter nitrogen pool'}
        ds['SoilN'].attrs={'units':'kgN/m2',
                           'long_name':'Soil nitrogen pool'}
        ds['Total'].attrs={'units':'kgN/m2',
                           'long_name':'Total nitrogen pool'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'VegN':{'dtype': 'float32'},
                                        'LitterN':{'dtype': 'float32'},
                                        'SoilN':{'dtype': 'float32'},
                                        'Total':{'dtype': 'float32'}})
                
    elif var == 'nsources':
        ds['dep'].attrs={'units':'gN/ha', 'long_name':'Deposition'}
        ds['fix'].attrs={'units':'gN/ha', 'long_name':'Fixation'}
        ds['fert'].attrs={'units':'gN/ha', 'long_name':'fertilization'}
        ds['input'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds['min'].attrs={'units':'gN/ha', 'long_name':'??'} 
        ds['imm'].attrs={'units':'gN/ha',
                         'long_name':'Nitrogen immobilisation'}
        ds['netmin'].attrs={'units':'gN/ha', 'long_name':'??'} 
        ds['Total'].attrs={'units':'gN/ha', 'long_name':'Total'}
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
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
        ds['Surf'].attrs={'units':'mm/year',  'long_name':'Surface runoff'} 
        ds['Drain'].attrs={'units':'mm/year', 'long_name':'??'}
        ds['Base'].attrs={'units':'mm/year', 'long_name':'??'}
        ds['Total'].attrs={'units':'mm/year', 'long_name':'??'} 
        
        # save to netCDF
        ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                        'Lat':{'dtype': 'double'},
                                        'Lon':{'dtype': 'double'},
                                        'Surf':{'dtype': 'float32'},
                                        'Drain':{'dtype': 'float32'},
                                        'Base':{'dtype': 'float32'},
                                        'Total':{'dtype': 'float32'}})
    else:
        pass
    
convert_ascii_netcdf('agpp', 'annual', 'LPJ-GUESS output CRUNCEP V7', '')
