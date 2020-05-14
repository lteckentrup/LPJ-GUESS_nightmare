import pandas as pd
import xarray
import os

pathwayIN= ''
pathwayOUT = ''
def convert_ascii_netcdf(var, time_res):
    
    # Import Data
    if time_res == 'monthly':      
        colnames = ['Lon', 'Lat', 'Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep',  'Oct', 'Nov', 'Dec']
    elif time_res == 'annual':
        if var in ('aaet', 'agpp', 'clitter', 'cmass', 'cton_leaf', 'dens', 
                   'npp', 'fpc', 'lai', 'nlitter', 'nmass', 'nuptake', 
                   'vmaxnlim'):
            colnames = ['Lon', 'Lat', 'Year', 'BNE', 'BINE', 'BNS', 'TeNE', 
                        'TeBS', 'IBS', 'TeBE', 'TrBE', 'TrIBE', 'TrBR', 'C3G', 
                        'C4G', 'Total']
        elif var in ('cflux'):
            colnames = ['Lon', 'Lat', 'Year', 'Veg', 'Repr', 'Soil', 'Fire', 
                        'Est', 'NEE']
        elif var == 'cpool':
            colnames = ['Lon', 'Lat', 'Year', 'VegC', 'LitterC', 'SoilC', 
                        'Total']
        elif var == 'doc':
            colnames = ['Lon', 'Lat', 'Year', 'Total']
        elif var == 'nflux':
            colnames = ['Lon', 'Lat', 'Year', 'dep', 'fix', 'fert', 'flux', 
                        'leach', 'NEE']
        elif var == 'ngases':
            colnames = ['Lon',  'Lat', 'Year', 'NH3', 'NOx', 'N2O', 'N2', 
                        'NSoil', 'Total']
        elif var == 'npool':
            colnames = ['Lon', 'Lat', 'Year', 'VegN', 'LitterN', 'SoilN', 
                        'Total']  
        elif var == 'nsources':
            colnames = ['Lon', 'Lat', 'Year', 'dep', 'fix', 'fert', 'input', 
                        'min', 'imm', 'netmin', 'Total']
        elif var == 'tot_runoff':
            colnames = ['Lon', 'Lat', 'Year', 'Surf', 'Drain', 'Base', 'Total']
        else:
            pass
    else:
        pass
    df = pd.read_csv('agpp.out',header=0,error_bad_lines=False, 
                     names=colnames,delim_whitespace=True)
    
    df2 = df.rename(columns={'Year': 'Time'})
    df_time = pd.date_range('1901-01-01', periods=115, freq='Y')
    
    
    print(df2)
    print(df2.set_index(['Time', 'Lat', 'Lon']))
    xr = df2.set_index(['Time', 'Lat', 'Lon']).to_xarray()
    
    # add metadata
    if time_res == 'monthly':
            xr['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
            xr['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}
            xr['Total'].attrs={'units':'kgC/m2/year', 'long_name':'Total'}
    elif time_res == 'annual':
            xr['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
            xr['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}
            xr['Time'].attrs={'units':'days since 1901-01-01', 
                              'long_name':'Time', 'calendar':'365_day'}

            if var in ('aaet', 'agpp', 'clitter', 'cmass', 'cton_leaf', 'dens', 
                       'npp', 'fpc', 'lai', 'nlitter', 'nmass', 'nuptake', 
                       'vmaxnlim'):
                xr['BNE'].attrs={'units':'kgC/m2/year',
                                 'long_name':'Boreal Needleleaved Evergreen tree'}
                xr['BINE'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Boreal Needleleaved Evergreen shade-Intolerant tree'}
                xr['BNS'].attrs={'units':'kgC/m2/year', 
                                 'long_name':'Boreal Needleleaved Summergreen tree'}
                xr['TeNE'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Temperate Needleleaved Evergreen tree'}
                xr['TeBS'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Temperate (shade-tolerant) Broadleaved Summergreen tree'}
                xr['IBS'].attrs={'units':'kgC/m2/year',
                                 'long_name':'boreal/ temperate shade-Intolerant Broadleaved Summergreen tree'}
                xr['TeBE'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Temperate Broadleaved Evergreen tree'}
                xr['TrBE'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Tropical Broadleaved Evergreen tree'}
                xr['TrIBE'].attrs={'units':'kgC/m2/year',
                                   'long_name':'Tropical Broadleaved Evergreen shade-Intolerant tree'}
                xr['TrBR'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Tropical Broadleaved Raingreen tree'}
                xr['C3G'].attrs={'units':'kgC/m2/year', 'long_name':'(cool) C3 Grass'}
                xr['C4G'].attrs={'units':'kgC/m2/year', 'long_name':'(warm) C4 Grass'}
                
                # save to netCDF
                xr.to_netcdf('agpp_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
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
                xr['Veg'].attrs={'units':'kgC/m2/year',
                                 'long_name':'Vegetation NPP'}
                xr['Repr'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Respired litter derived from plant allocation to reproduction'}
                xr['Soil'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Soil heterotrophic respiration'}
                xr['Fire'].attrs={'units':'kgC/m2/year',
                                  'long_name':'Wildfire emissions'}
                xr['Est'].attrs={'units':'kgC/m2/year',
                                 'long_name':'Biomass of plants establishing in the current year'}
                xr['NEE'].attrs={'units':'kgC/m2/year', 'long_name':'Net C flux (sum of other fluxes'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'Veg':{'dtype': 'float32'},
                                       'Repr':{'dtype': 'float32'},
                                       'Soil':{'dtype': 'float32'},
                                       'Fire':{'dtype': 'float32'},
                                       'Est':{'dtype': 'float32'},
                                       'NEE':{'dtype': 'float32'}})
            elif var == 'cpool':
                xr['VegC'].attrs={'units':'kgC/m2',
                                  'long_name':'Vegetation carbon pool'}
                xr['LitterC'].attrs={'units':'kgC/m2',
                                     'long_name':'Litter carbon pool'}
                xr['SoilC'].attrs={'units':'kgC/m2',
                                   'long_name':'Soil carbon pool'}
                xr['Total'].attrs={'units':'kgC/m2',
                                   'long_name':'Total carbon pool'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'VegC':{'dtype': 'float32'},
                                       'LitterC':{'dtype': 'float32'},
                                       'SoilC':{'dtype': 'float32'},
                                       'Total':{'dtype': 'float32'}})
            elif var == 'doc':
                xr['Total'].attrs={'units':'kgC/m2r',
                                   'long_name':'Total dissolved organic carbon'}
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'Total':{'dtype': 'float32'}})
            elif var == 'nflux':
                xr['dep'].attrs={'units':'kgN/ha',
                                 'long_name':'Deposition'}
                xr['fix'].attrs={'units':'kgN/ha',
                                 'long_name':'Fixation'}
                xr['fert'].attrs={'units':'kgN/ha',
                                  'long_name':'fertilization'}
                xr['flux'].attrs={'units':'kgN/ha',
                                  'long_name':'Soil emission'}
                xr['leach'].attrs={'units':'kgN/ha',
                                   'long_name':'leaching'}
                xr['NEE'].attrs={'units':'kgN/ha',
                                 'long_name':'Net N flux (sum of other fluxes)'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'dep':{'dtype': 'float32'},
                                       'fix':{'dtype': 'float32'},
                                       'fert':{'dtype': 'float32'},
                                       'flux':{'dtype': 'float32'},
                                       'leach':{'dtype': 'float32'},
                                       'NEE':{'dtype': 'float32'}})
                
                
            elif var == 'ngases':
                colnames = ['Lon',  'Lat', 'Year', 'NH3', 'NOx', 'N2O', 'N2',
                            'NSoil', 'Total']
                xr['NH3'].attrs={'units':'kgN/ha/year',
                                 'long_name':'NH3 flux to atmosphere from fire'}
                xr['NOx'].attrs={'units':'kgN/ha/year',
                                 'long_name':'NOx flux to atmosphere from fire'}
                xr['N2O'].attrs={'units':'kgN/ha/year',
                                 'long_name':'N2O flux to atmosphere from fire'}
                xr['N2'].attrs={'units':'kgN/ha',
                                'long_name':'N2O flux to atmosphere from fire'}
                xr['NSoil'].attrs={'units':'kgN/ha',
                                   'long_name':'??'}
                xr['Total'].attrs={'units':'kgN/ha',
                                   'long_name':'Total'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'NH3':{'dtype': 'float32'},
                                       'NOx':{'dtype': 'float32'},
                                       'N2O':{'dtype': 'float32'},
                                       'N2':{'dtype': 'float32'},
                                       'NSoil':{'dtype': 'float32'},
                                       'Total':{'dtype': 'float32'}})            
                
            elif var == 'npool':
                xr['VegN'].attrs={'units':'kgN/m2',
                                  'long_name':'Vegetation nitrogen pool'}
                xr['LitterN'].attrs={'units':'kgN/m2',
                                     'long_name':'Litter nitrogen pool'}
                xr['SoilN'].attrs={'units':'kgN/m2',
                                   'long_name':'Soil nitrogen pool'}
                xr['Total'].attrs={'units':'kgN/m2',
                                   'long_name':'Total nitrogen pool'}
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'VegN':{'dtype': 'float32'},
                                       'LitterN':{'dtype': 'float32'},
                                       'SoilN':{'dtype': 'float32'},
                                       'Total':{'dtype': 'float32'}})
                
            elif var == 'nsources':
                xr['dep'].attrs={'units':'gN/ha',
                                 'long_name':'Deposition'}
                xr['fix'].attrs={'units':'gN/ha',
                                 'long_name':'Fixation'}
                xr['fert'].attrs={'units':'gN/ha',
                                  'long_name':'fertilization'}
                xr['input'].attrs={'units':'gN/ha',
                                   'long_name':'??'}
                xr['min'].attrs={'units':'gN/ha',
                                 'long_name':'??'}
                xr['imm'].attrs={'units':'gN/ha',
                                 'long_name':'Nitrogen immobilisation'}
                xr['netmin'].attrs={'units':'gN/ha',
                                    'long_name':'??'} 
                xr['Total'].attrs={'units':'gN/ha',
                                   'long_name':'Total'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
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
                colnames = ['Lon', 'Lat', 'Year', 'Surf', 'Drain', 'Base',
                            'Total']
                xr['Surf'].attrs={'units':'mm/year',
                                  'long_name':'Surface runoff'}
                xr['Drain'].attrs={'units':'mm/year',
                                   'long_name':'??'}
                xr['Base'].attrs={'units':'mm/year',
                                  'long_name':'??'}
                xr['Total'].attrs={'units':'mm/year',
                                   'long_name':'??'}
                
                # save to netCDF
                xr.to_netcdf(pathway_OUT+var+'_LPJ-GUESS_1901-2015.nc',
                             encoding={'Time':{'dtype': 'double'},
                                       'Lat':{'dtype': 'double'},
                                       'Lon':{'dtype': 'double'},
                                       'Surf':{'dtype': 'float32'},
                                       'Drain':{'dtype': 'float32'},
                                       'Base':{'dtype': 'float32'},
                                       'Total':{'dtype': 'float32'}})
            else:
                pass
            

    
    # add global attribute metadata
    # xr.attrs={'Conventions':'CF-1.6', 'title':'Data', 'summary':'Data generated'}
    
convert_ascii_netcdf('agpp', 'annual')
