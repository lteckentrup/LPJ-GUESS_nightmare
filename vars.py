### LPJ GUESS PFT and variable abbreviations and long names

PFT_shortnames=['BNE', 'BINE', 'BNS', 'TeNE', 'TeBS', 'IBS', 'TeBE',  'TrBE',
                'TrIBE', 'TrBR', 'C3G', 'C4G']
PFT_longnames=['Boreal Needleleaved Evergreen Tree',
               'Boreal Shade Intolerant Needleleaved Evergreen Tree',
               'Boreal Needleleaved Summergreen Tree',
               'Temperate Needleleaved Evergreen Tree',
               'Temperate (Shade-tolerant) Broadleaved Summergreen Tree',
               'Boreal/ temperate Shade-intolerant Broadleaved Summergreen Tree',
               'Temperate Broadleaved Evergreen Tree',
               'Tropical Broadleaved Evergreen Tree',
               'Tropical Shade-intolerant Broadleaved Evergreen Tree',
               'Tropical Broadleaved Raingreen Tree',
               'C3 Grass',
               'C4 Grass']

# BA_shortname = 'BurntFr'
# BA_longname = 'Burnt Area Fraction'

BA_shortname = 'BurntAr'
BA_longname = 'Burnt Area'

cflux_shortnames=['Veg', 'Repr', 'Soil', 'Fire', 'Est', 'NEE']
cflux_longnames=['Vegetation NPP',
                 'Respired litter derived from plant allocation to reproduction',
                 'Soil heterotrophic respiration',
                 'Wildfire carbon emissions',
                 'Biomass of plants establishing in the current year',
                 'Net C flux (sum of other fluxes']

cpool_shortnames=['VegC', 'LitterC', 'SoilC', 'Total']
cpool_longnames=['Vegetation carbon pool',
                 'Litter carbon pool',
                 'Soil carbon pool',
                 'Total carbon pool']

firert_shortnames=['FireRT', 'BurntFr']
firert_longnames=['Fire return time',
                  'Burnt Area Fraction']

nflux_shortnames=['dep', 'fix', 'fert', 'flux', 'leach', 'NEE']
nflux_longnames=['Deposition',
                 'Fixation',
                 'Fertilization',
                 'Soil emission',
                 'Leaching',
                 'Net N flux (sum of other fluxes)']

ngases_shortnames=['NH3', 'NOx', 'N2O', 'N2', 'NSoil', 'Total']
ngases_longnames=['NH3 flux to atmosphere from fire',
                  'NOx flux to atmosphere from fire',
                  'N2O flux to atmosphere from fire',
                  'N2 flux to atmosphere from fire',
                  'N flux to soil from fire',
                  'Total Nflux']

npool_shortnames=['VegN', 'LitterN', 'SoilN', 'Total']
npool_longnames=['Vegetation nitrogen pool',
                 'Litter nitrogen pool',
                 'Soil nitrogen pool',
                 'Total nitrogen pool']

nsources_shortnames=['dep', 'fix', 'fert', 'input', 'min', 'imm', 'netmin',
                     'Total']
nsources_longnames=['Deposition',
                    'Fixation',
                    'Fertilization',
                    '??',
                    '??',
                    'Nitrogen immobilisation',
                    '??',
                    'Total']

simfire_analysis_shortnames = ['Biome', 'MxNest', 'PopDens', 'AMxFApar', 'FireProb', 'Region']
simfire_analysis_longnames = ['Biome', 'Maximum Nesterov Index', 'Population Density',
                              'Maximum FaPAR', 'Fire Probability', 'Region']

tot_runoff_shortnames=['Surf', 'Drain', 'Base', 'Total']
tot_runoff_longnames=['Surface runoff',
                      'Subsurface Drainage',
                      'Baseflow runoff',
                      'Total runoff']
