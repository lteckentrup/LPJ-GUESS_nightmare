import pandas as pd
import xarray
import os

# Import Data
colnames = ['Lon', 'Lat', 'Year', 'BNE', 'BINE', 'BNS', 'TeNE', 'TeBS', 'IBS',
            'TeBE', 'TrBE', 'TrIBE', 'TrBR', 'C3G', 'C4G', 'Total']
df = pd.read_csv('agpp_old.out',header=0,error_bad_lines=False, 
                 names=colnames,delim_whitespace=True)

df2 = df.rename(columns={'Year': 'Time'})

xr = df2.set_index(['Time', 'Lat', 'Lon']).to_xarray()

# add metadata
xr['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
xr['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}
xr['Total'].attrs={'units':'kgC/m2/year', 'long_name':'Total'}
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
                  'long_name':' Tropical Broadleaved Evergreen tree'}
xr['TrIBE'].attrs={'units':'kgC/m2/year', 
                   'long_name':'Tropical Broadleaved Evergreen shade-Intolerant tree'}
xr['TrBR'].attrs={'units':'kgC/m2/year', 
                  'long_name':'Tropical Broadleaved Raingreen tree'}
xr['C3G'].attrs={'units':'kgC/m2/year', 'long_name':'(cool) C3 Grass'}
xr['C4G'].attrs={'units':'kgC/m2/year', 'long_name':'(warm) C4 Grass'}

# add global attribute metadata
# xr.attrs={'Conventions':'CF-1.6', 'title':'Data', 'summary':'Data generated'}

# save to netCDF
xr.to_netcdf('test.nc', encoding={'Time':{'dtype': 'double'},
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
