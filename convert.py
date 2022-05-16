from write_netcdf import (
    ascii2netcdf
    )

'''
convert_ascii_netcdf_monthly(var, experiment)
convert_ascii_netcdf_annual(var, experiment)
'''

### Convert annual GPP 
convert_ascii_netcdf_annual('agpp')

### Convert monthly total GPP
convert_ascii_netcdf_monthly('mgpp', '')

### Convert monthly C4G GPP
convert_ascii_netcdf_monthly('mgpp', 'C4G')
